import re
import functools
import subprocess
from collections import defaultdict


HOOKS = defaultdict(list)


def get_active_hooks(hook_type):
    return HOOKS.get(hook_type, [])


def prepare_commit_msg_hook(fn):
    @functools.wraps(fn)
    def wrapper(temp_msg_file):
        return fn(temp_msg_file)

    HOOKS['prepare-commit-msg'].append(wrapper)
    return wrapper


@prepare_commit_msg_hook
def append_jira_ticket_id(temp_msg_file):
    """If you name your branch using the following scheme:

        issue-NNNNN-description
        JIRAPROJECT-NNNNN-description

    this prepare_commit_msg hook will prepend your comment message
    with `issue-NNNNN` or `JIRAPROJECT-NNNNN`
    """
    branch_name = subprocess.check_output('git symbolic-ref --short HEAD', shell=True).strip()
    if '-' not in branch_name:
        return
    parts = branch_name.split('-')
    jira_ticket = '-'.join(parts[:2])
    with open(temp_msg_file, 'r') as fh:
        msg = fh.read()

    msg = '{}: {}'.format(jira_ticket, msg)
    with open(temp_msg_file, 'w') as fh:
        fh.write(msg)
