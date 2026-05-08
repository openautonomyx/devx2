import json
import urllib.request
import os


class GitHubAdapter:
    def __init__(self):
        self.token = os.environ.get('GITHUB_TOKEN')
        self.repo = os.environ.get('GITHUB_REPOSITORY')

    def request(self, method: str, path: str, payload=None):
        url = f'https://api.github.com/repos/{self.repo}{path}'

        data = json.dumps(payload).encode('utf-8') if payload else None

        req = urllib.request.Request(
            url,
            data=data,
            headers={
                'Authorization': f'Bearer {self.token}',
                'Accept': 'application/vnd.github+json',
                'X-GitHub-Api-Version': '2022-11-28',
                'Content-Type': 'application/json',
            },
            method=method,
        )

        with urllib.request.urlopen(req) as res:
            return res.read().decode('utf-8')

    def comment_on_issue(self, issue_number: str, body: str):
        return self.request(
            'POST',
            f'/issues/{issue_number}/comments',
            {'body': body},
        )
