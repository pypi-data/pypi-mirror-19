# This file is part of jenkins-epo
#
# jenkins-epo is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or any later version.
#
# jenkins-epo is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# jenkins-epo.  If not, see <http://www.gnu.org/licenses/>.

from copy import deepcopy
import datetime
import inspect
import logging
import pkg_resources
import random
import socket

from jenkins_yml.job import Job as JobSpec

from ..bot import Extension, Error, SkipHead
from ..github import GITHUB, ApiError, ApiNotFoundError
from ..repository import Branch, CommitStatus
from ..settings import SETTINGS
from ..utils import deepupdate, match, parse_patterns


logger = logging.getLogger(__name__)


class AutoCancelExtension(Extension):
    stage = '30'

    def run(self):
        payload = self.current.head.fetch_previous_commits()
        commits = self.current.repository.process_commits(payload)
        head = True
        for i, commit in enumerate(commits):
            commit_payload = commit.fetch_statuses()
            statuses = commit.process_statuses(commit_payload)
            for status in statuses.values():
                status = CommitStatus(status)
                if status.get('state') != 'pending':
                    continue

                if status.is_queueable:
                    continue

                if head:
                    self.current.poll_queue.append((commit, status))
                else:
                    logger.info("Queue cancel of %s on %s.", status, commit)
                    self.current.cancel_queue.append((commit, status))

            head = False


class HelpExtension(Extension):
    stage = '90'

    DEFAULTS = {
        'help_mentions': set(),
    }
    DISTRIBUTION = pkg_resources.get_distribution('jenkins-epo')
    HELP = """\
<!--
jenkins: ignore
-->

%(mentions)s: this is what I understand:

```yaml
# Build this PR first. Allowed only in PR description.
jenkins: urgent

%(help)s
```

You can mix instructions. Multiline instructions **must** be in code block.

--
*%(me)s for your service*

<!--
jenkins: [process, help-reset]

Running %(software)s==%(version)s on %(host)s
Extensions: %(extensions)s
-->
"""

    def process_instruction(self, instruction):
        if instruction.name in ('help', 'man'):
            self.current.help_mentions.add(instruction.author)
        elif instruction == 'help-reset':
            self.current.help_mentions = set()

    def generate_comment(self):
        docs = []
        for ext in self.bot.extensions:
            doc = ext.__class__.__doc__
            if not doc:
                continue
            docs.append(inspect.cleandoc(doc))
        help_ = '\n\n'.join(docs)
        return self.HELP % dict(
            extensions=','.join(sorted(self.bot.extensions_map.keys())),
            help=help_,
            host=socket.getfqdn(),
            me=self.current.head.repository.SETTINGS.NAME,
            mentions=', '.join(sorted([
                '@' + m for m in self.current.help_mentions
            ])),
            software=self.DISTRIBUTION.project_name,
            version=self.DISTRIBUTION.version,
        )

    def run(self):
        if self.current.help_mentions:
            self.current.head.comment(body=self.generate_comment())


class ErrorExtension(Extension):
    stage = '99'

    ERROR_COMMENT = """
%(emoji)s

%(error)s

<!--
jenkins: reset-errors
-->
"""  # noqa

    DEFAULTS = {
        'error_reset': None,
    }

    def process_instruction(self, instruction):
        if instruction == 'reset-errors':
            self.current.error_reset = instruction.date

    def run(self):
        reset = self.current.error_reset
        for error in self.current.errors:
            if reset and error.date < reset:
                continue

            self.current.head.comment(body=self.ERROR_COMMENT % dict(
                emoji=random.choice((
                    ':see_no_evil:', ':bangbang:', ':confused:',
                )),
                error=error.body,
            ))


class MergerExtension(Extension):
    """
    # Acknowledge for auto-merge
    jenkins: opm
    """

    stage = '90'

    DEFAULTS = {
        'opm': None,
        'opm_denied': [],
        'opm_processed': None,
        'last_merge_error': None,
    }

    SETTINGS = {
        'WIP_TITLE': 'wip*,[wip*',
    }

    OPM_COMMENT = """
%(mention)s, %(message)s %(emoji)s

<!--
jenkins: opm-processed
-->
"""

    MERGE_ERROR_COMMENT = """
%(mention)s, %(message)s %(emoji)s

<!--
jenkins: {last-merge-error: %(message)r}
-->
"""

    def begin(self):
        super(MergerExtension, self).begin()

        if hasattr(self.current.head, 'merge'):
            patterns = parse_patterns(self.current.SETTINGS.WIP_TITLE.lower())
            title = self.current.head.payload['title'].lower()
            self.current.wip = match(title, patterns)
            if self.current.wip:
                logger.debug("%s is a WIP.", self.current.head)

    def process_instruction(self, instruction):
        if instruction in {'lgtm', 'merge', 'opm'}:
            self.process_opm(instruction)
        elif instruction in {'lgtm-processed', 'opm-processed'}:
            self.current.opm_denied[:] = []
            self.current.opm_processed = instruction
        elif instruction == 'last-merge-error':
            self.current.last_merge_error = instruction

    def process_opm(self, opm):
        if not hasattr(self.current.head, 'merge'):
            return logger.debug("OPM on a non PR. Weird!")

        if opm.date < self.current.last_commit.date:
            return logger.debug("Skip outdated OPM.")

        if opm.author in self.current.SETTINGS.REVIEWERS:
            logger.info("Accept @%s as reviewer.", opm.author)
            self.current.opm = opm
        else:
            logger.info("Refuse OPM from @%s.", opm.author)
            self.current.opm_denied.append(opm)

    def run(self):
        denied = {i.author for i in self.current.opm_denied}
        if denied:
            self.current.head.comment(body=self.OPM_COMMENT % dict(
                emoji=random.choice((
                    ':confused:', ':cry:', ':disappointed:', ':frowning:',
                    ':scream:',
                )),
                mention=', '.join(sorted(['@' + a for a in denied])),
                message="you're not allowed to acknowledge PR",
            ))

        if not self.current.opm:
            return
        logger.debug("Accept to merge for @%s.", self.current.opm.author)

        if self.current.wip:
            logger.info("Not merging WIP PR.")
            proc = self.current.opm_processed
            if proc and proc.date > self.current.opm.date:
                return

            self.current.head.comment(body=self.OPM_COMMENT % dict(
                emoji=random.choice((
                    ':confused:', ':hushed:', ':no_mouth:', ':open_mouth:',
                )),
                mention='@' + self.current.opm.author,
                message="this PR is still WIP",
            ))
            return

        status = self.current.last_commit.fetch_combined_status()
        if status['state'] != 'success':
            return logger.debug("PR not green. Postpone merge.")

        try:
            self.current.head.merge()
        except ApiError as e:
            error = e.response['json']['message']
            if self.current.last_merge_error:
                last_error = self.current.last_merge_error.args
                if error == last_error:
                    return logger.debug("Merge still failing: %s", error)

            logger.warn("Failed to merge: %s", error)
            self.current.head.comment(body=self.MERGE_ERROR_COMMENT % dict(
                emoji=random.choice((':confused:', ':disappointed:')),
                mention='@' + self.current.opm.author, message=error,
            ))
        else:
            logger.warn("Merged %s!", self.current.head)
            self.current.head.delete_branch()


class OutdatedExtension(Extension):
    stage = '00'

    SETTINGS = {
        'COMMIT_MAX_WEEKS': 4,
    }

    def begin(self):
        weeks = self.current.SETTINGS.COMMIT_MAX_WEEKS
        maxage = datetime.timedelta(weeks=weeks)
        age = datetime.datetime.utcnow() - self.current.last_commit.date
        if age > maxage:
            logger.debug(
                'Skipping %s because older than %s weeks.',
                self.current.head, self.current.SETTINGS.COMMIT_MAX_WEEKS,
            )
            raise SkipHead()


class ReportExtension(Extension):
    stage = '90'

    ISSUE_TEMPLATE = """
Commit %(abbrev)s is broken on %(branch)s:

%(builds)s
"""
    COMMENT_TEMPLATE = """
Build failure reported at #%(issue)s.

<!--
jenkins: report-done
-->
"""

    DEFAULTS = {
        # Issue URL where the failed builds are reported.
        'report_done': False,
    }

    def process_instruction(self, instruction):
        if instruction == 'report-done':
            self.current.report_done = True

    def run(self):
        if self.current.report_done:
            return

        if not isinstance(self.current.head, Branch):
            return

        errored = [
            s for s in self.current.statuses.values()
            if s['state'] == 'failure'
        ]
        if not errored:
            return

        branch_name = self.current.head.ref[len('refs/heads/'):]
        builds = '- ' + '\n- '.join([s['target_url'] for s in errored])
        issue = self.current.head.repository.report_issue(
            title="%s is broken" % (branch_name,),
            body=self.ISSUE_TEMPLATE % dict(
                abbrev=self.current.head.sha[:7],
                branch=branch_name,
                builds=builds,
                sha=self.current.head.sha,
                ref=self.current.head.ref,
            )
        )

        self.current.head.comment(body=self.COMMENT_TEMPLATE % dict(
            issue=issue['number']
        ))


class SkipExtension(Extension):
    """
    jenkins: skip  # Skip all jobs

    # Selecting jobs
    jenkins:
      jobs: only*
      jobs: ['this*', '+andthis*', '-notthis*']
    """

    stage = '30'

    DEFAULTS = {
        'jobs_match': [],
    }
    BUILD_ALL = ['*']

    def process_instruction(self, instruction):
        if instruction == 'skip':
            self.current.jobs_match = ['!*']
        elif instruction == 'jobs':
            patterns = instruction.args
            if isinstance(patterns, str):
                patterns = [patterns]
            self.current.jobs_match = patterns

    def run(self):
        for name, spec in self.current.job_specs.items():
            job = self.current.jobs[name]
            for context in job.list_contexts(spec):
                if match(context, self.current.jobs_match):
                    continue

                status = self.current.statuses.get(context, CommitStatus())
                if status.get('state') == 'success':
                    continue

                if status.is_running:
                    self.current.cancel_queue.append(
                        (self.current.last_commit, status)
                    )

                logger.info("Skipping %s.", context)
                self.current.last_commit.maybe_update_status(CommitStatus(
                    context=context, target_url=job.baseurl,
                    state='success', description='Skipped!',
                ))


class YamlExtension(Extension):
    """
    # Ephemeral jobs parameters
    jenkins:
      parameters:
        job1:
          PARAM: value
    """
    stage = '00'

    DEFAULTS = {
        'yaml': {},
        'yaml_date': None,
    }

    SETTINGS = {
        # Jenkins credentials used to clone
        'JOBS_CREDENTIALS': None,
        # Jenkins node/label
        'JOBS_NODE': 'yml',
    }

    def process_instruction(self, instruction):
        if instruction.name in {'yaml', 'yml'}:
            if not isinstance(instruction.args, dict):
                self.current.errors.append(
                    Error("YAML args is not a mapping.", instruction.date)
                )
                return
            deepupdate(self.current.yaml, instruction.args)
            self.current.yaml_date = instruction.date
        elif instruction.name in {'parameters', 'params', 'param'}:
            args = {}
            for job, parameters in instruction.args.items():
                args[job] = dict(parameters=parameters)
            deepupdate(self.current.yaml, args)
            self.current.yaml_date = instruction.date

    def list_job_specs(self, jenkins_yml=None):
        defaults = dict(
            node=SETTINGS.JOBS_NODE,
            github_repository=self.current.head.repository.url,
            scm_credentials=SETTINGS.JOBS_CREDENTIALS,
            set_commit_status=not SETTINGS.DRY_RUN,
        )

        jenkins_yml = jenkins_yml or '{}'
        jobs = {}
        for job in JobSpec.parse_all(jenkins_yml, defaults=defaults):
            job.repository = self.current.head.repository
            jobs[job.name] = job

        return jobs

    def run(self):
        head = self.current.head

        try:
            jenkins_yml = GITHUB.fetch_file_contents(
                head.repository, 'jenkins.yml', ref=head.ref,
            )
            logger.debug("Loading jenkins.yml.")
        except ApiNotFoundError:
            jenkins_yml = None

        try:
            self.current.job_specs = self.list_job_specs(jenkins_yml)
        except Exception as e:
            self.current.errors.append(Error(
                "Failed to load `jenkins.yml`:\n\n```\n%s\n```" % (e,),
                self.current.last_commit.date
            ))
            return

        self.current.jobs = head.repository.jobs

        for name, args in self.current.yaml.items():
            if name not in self.current.job_specs:
                self.current.errors.append(Error(
                    body="Can't override unknown job %s." % (name,),
                    date=self.current.yaml_date,
                ))
                continue

            current_spec = self.current.job_specs[name]
            config = dict(deepcopy(current_spec.config), **args)
            overlay_spec = JobSpec(name, config)
            logger.info("Ephemeral update of %s spec.", name)
            self.current.job_specs[name] = overlay_spec
