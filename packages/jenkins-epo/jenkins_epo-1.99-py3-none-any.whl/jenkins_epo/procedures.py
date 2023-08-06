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

import asyncio
from datetime import datetime, timedelta
import itertools
import logging

from .github import GITHUB, cached_arequest
from .repository import Repository
from .settings import SETTINGS
from .utils import retry


logger = logging.getLogger(__name__)


def iter_heads():
    queues = []

    for repository in list_repositories():
        logger.info("Fetching %s heads.", repository)
        branches = repository.fetch_protected_branches()
        pulls = repository.fetch_pull_requests()
        heads = reversed(sorted(itertools.chain(
            repository.process_protected_branches(branches),
            repository.process_pull_requests(pulls),
        ), key=lambda head: head.sort_key()))

        # Yield first head of the repository before loading next repositories.
        queue = iter(heads)
        try:
            yield next(heads)
        except StopIteration:
            continue
        except GeneratorExit:
            return
        else:
            queues.append(queue)

    while queues:
        for queue in queues[:]:
            try:
                yield next(queue)
            except StopIteration:
                queues.remove(queue)
            except GeneratorExit:
                return


def list_repositories(with_settings=False):
    repositories = set()

    env_repos = filter(
        None,
        SETTINGS.REPOSITORIES.replace(' ', ',').split(',')
    )
    for repository in env_repos:
        if repository in repositories:
            continue
        owner, name = repository.split('/')
        try:
            repository = Repository.from_name(owner, name)
        except Exception as e:
            logger.warn("Failed to fetch repo %s: %s", repository, e)
            if SETTINGS.DEBUG:
                raise
            else:
                continue

        if repository in repositories:
            continue

        repositories.add(repository)
        logger.debug("Managing %s.", repository)
        yield repository


@asyncio.coroutine
def whoami():
    user = yield from cached_arequest(GITHUB.user)
    logger.info("I'm @%s on GitHub.", user['login'])
    return user['login']


def compute_throttling(now, rate_limit):
    now = now.replace(microsecond=0)
    # https://developer.github.com/v3/#rate-limiting
    time_limit = 3600
    reset = datetime.utcfromtimestamp(rate_limit['rate']['reset'])
    time_remaining = (reset - now).seconds

    calls_limit = rate_limit['rate']['limit'] - SETTINGS.RATE_LIMIT_THRESHOLD
    calls_remaining = (
        rate_limit['rate']['remaining'] - SETTINGS.RATE_LIMIT_THRESHOLD
    )

    time_consumed = time_limit - time_remaining
    calls_consumed = calls_limit - calls_remaining
    countdown = calls_limit / calls_consumed * time_consumed - time_consumed
    estimated_end = now + timedelta(seconds=int(countdown))

    logger.info(
        "%d remaining API calls estimated to end by %s UTC.",
        calls_remaining, estimated_end,
    )
    logger.info("GitHub API rate limit reset at %s UTC.", reset)

    if countdown > time_remaining:
        return 0
    else:
        # Split processing time by slot of 30s. Sleep between them.
        slots_count = countdown / 30
        estimated_sleep = time_remaining - countdown
        return estimated_sleep / slots_count


@retry
@asyncio.coroutine
def throttle_github():
    now = datetime.utcnow()
    payload = yield from GITHUB.rate_limit.aget()
    seconds_to_wait = compute_throttling(now, payload)
    if seconds_to_wait:
        logger.warn("Throttling GitHub API calls by %ds.", seconds_to_wait)
        yield from asyncio.sleep(seconds_to_wait)
