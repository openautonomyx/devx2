import os
import json
import urllib.request
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

SYSTEM_PROMPT = '''
You are the devx2 Project Driver Agent.

devx2 is a composable, self-hostable, cloud-native software delivery platform
built on CNCF technologies and delivered through an open-core model.

Responsibilities:
- review roadmap and issues
- decompose work into milestones
- suggest architecture tasks
- create implementation plans
- draft developer tasks
- identify blockers and risks
- maintain momentum across the project

When responding to GitHub issues or pull requests, be concise, actionable, and structured.
Always include recommended next steps.
'''


def run_agent(task: str) -> str:
    response = client.responses.create(
        model=os.environ.get('OPENAI_MODEL', 'gpt-5.1'),
        input=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': task},
        ],
    )

    return response.output_text


def post_github_comment(body: str) -> None:
    token = os.environ.get('GITHUB_TOKEN')
    repo = os.environ.get('GITHUB_REPOSITORY')
    issue_number = os.environ.get('GITHUB_ISSUE_NUMBER')

    if not token or not repo or not issue_number:
        return

    url = f'https://api.github.com/repos/{repo}/issues/{issue_number}/comments'
    payload = json.dumps({'body': body}).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            'Authorization': f'Bearer {token}',
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
            'Content-Type': 'application/json',
        },
        method='POST',
    )

    with urllib.request.urlopen(req) as res:
        res.read()


if __name__ == '__main__':
    task = os.environ.get(
        'PROJECT_DRIVER_TASK',
        'Review current project state and propose next implementation steps.'
    )

    output = run_agent(task)
    print(output)

    comment = f'''## devx2 Project Driver Agent\n\n{output}\n\n---\n_Automated by the devx2 OpenAI SDK project driver._'''
    post_github_comment(comment)
