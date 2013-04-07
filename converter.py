import argparse
import itertools
import json
import zipfile

parser = argparse.ArgumentParser(description='Export GitHub issues to Bitbucket format.')
parser.add_argument('username')
parser.add_argument('password')
parser.add_argument('repo_user')
parser.add_argument('repo_name')
args = parser.parse_args()

from github3 import login, GitHubError

try:
    gh = login(args.username, args.password)
except GitHubError:
    parser.exit(1, "Invalid credentials.\n")

repo = gh.repository(args.repo_user, args.repo_name)
if not repo:
    parser.exit(1, "Invalid repository.\n")

meta = {
    'default_kind': 'bug'
}
issues = []
comments = []
milestones = []

for issue in itertools.chain(repo.iter_issues(), repo.iter_issues(state='closed')):
    issues.append({
        'id': issue.id,
        'created_on': issue.created_at.isoformat(),
        'updated_on': issue.updated_at.isoformat(),
        'content_updated_on': issue.updated_at.isoformat(),
        'assignee': issue.assignee.login if issue.assignee else None,
        'reporter': issue.user.login,
        'milestone': issue.milestone.title if issue.milestone else None,
        'title': issue.title,
        'content': issue.body,
        'status': 'resolved' if issue.is_closed() else 'open',
        'kind': 'bug', # todo: determine based on labels
        'priority': 'minor' # todo: determine based on labels
    })

    if issue.comments > 0:
        for comment in issue.iter_comments():
            comments.append({
                'id': comment.id,
                'content': comment.body,
                'created_on': comment.created_at.isoformat(),
                'updated_on': comment.updated_at.isoformat(),
                'issue': issue.id,
                'user': comment.user.login
            })

for milestone in repo.iter_milestones():
    milestones.append({
        'name': milestone.title
    })

output = {
    'meta': meta,
    'issues': issues,
    'comments': comments,
    'milestones': milestones
}

with zipfile.ZipFile(repo.name + '.zip', 'w') as z:
    z.writestr('db-1.0.json', json.dumps(output))
