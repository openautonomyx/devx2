import os
import json
import urllib.request
from openai import OpenAI

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

SYSTEM_PROMPT = '''
You are the devx2 Project Driver Agent.

devx2 is a composable, self-hostable, cloud-native software delivery platform
built on CNCF technologies and delivered through an open-core model.

Mission:
- keep the project moving
- turn product direction into actionable engineering work
- protect the composable CNCF-native architecture
- identify blockers, risks, and missing decisions

Operating modes:
- planning: decompose product direction into milestones and issues
- architecture-review: review designs for composability, self-hostability, security, CNCF alignment, and open-core boundaries
- sprint-planning: propose the next sprint backlog
- issue-triage: convert rough issues into scoped tasks

When responding to GitHub issues or pull requests:
- be concise and actionable
- use markdown checklists
- include owners as role suggestions, not named people
- include acceptance criteria
- include recommended next steps
'''


def github_request(method: str, path: str, payload: dict | None = None):
    token = os.environ.get('GITHUB_TOKEN')
    repo = os.environ.get('GITHUB_REPOSITORY')
    if not token or not repo:
        return None

    url = f'https://api.github.com/repos/{repo}{path}'
    data = json.dumps(payload).encode('utf-8') if payload is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            'Authorization': f'Bearer {token}',
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
            'Content-Type': 'application/json',
        },
        method=method,
    )
    with urllib.request.urlopen(req) as res:
        body = res.read().decode('utf-8')
        return json.loads(body) if body else None


def run_agent(task: str) -> str:
    mode = os.environ.get('PROJECT_DRIVER_MODE', 'planning')
    response = client.responses.create(
        model=os.environ.get('OPENAI_MODEL', 'gpt-5.1'),
        input=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': f'Mode: {mode}\n\nTask:\n{task}'},
        ],
    )
    return response.output_text


def post_github_comment(body: str) -> None:
    issue_number = os.environ.get('GITHUB_ISSUE_NUMBER')
    if not issue_number:
        return
    github_request('POST', f'/issues/{issue_number}/comments', {'body': body})


def create_issue(title: str, body: str, labels: list[str] | None = None) -> None:
    github_request('POST', '/issues', {'title': title, 'body': body, 'labels': labels or []})


def seed_mvp_issues() -> None:
    issues = [
        (
            'MVP: Define platform-core service boundaries',
            '## Goal\nDefine the initial service/module boundaries for devx2 platform-core.\n\n## Acceptance Criteria\n- [ ] Define control plane responsibilities\n- [ ] Define API boundaries for services, deployments, environments, and providers\n- [ ] Document OSS vs enterprise boundaries\n- [ ] Add architecture notes under docs/\n\n## Suggested owner\nPlatform engineering',
            ['mvp', 'architecture']
        ),
        (
            'MVP: Implement Forge Gateway provider interface',
            '## Goal\nCreate the initial SCM abstraction interface for GitHub, GitLab, and Forgejo.\n\n## Acceptance Criteria\n- [ ] Define provider interface\n- [ ] Add GitHub adapter skeleton\n- [ ] Add GitLab adapter skeleton\n- [ ] Add Forgejo adapter skeleton\n- [ ] Normalize webhook event model\n\n## Suggested owner\nBackend/platform',
            ['mvp', 'forge-gateway']
        ),
        (
            'MVP: Add Backstage service template for demo app',
            '## Goal\nCreate the first golden-path template for a demo microservice.\n\n## Acceptance Criteria\n- [ ] Scaffold service repo layout\n- [ ] Generate Tekton pipeline manifest\n- [ ] Generate Argo CD Application manifest\n- [ ] Generate Harbor image naming convention\n- [ ] Add README usage docs\n\n## Suggested owner\nDeveloper experience',
            ['mvp', 'backstage', 'templates']
        ),
        (
            'MVP: Add Tekton build pipeline skeleton',
            '## Goal\nCreate a reusable Tekton pipeline for build, test, image push, and GitOps update.\n\n## Acceptance Criteria\n- [ ] Build step\n- [ ] Test step\n- [ ] OCI image push step\n- [ ] GitOps manifest update step\n- [ ] Example PipelineRun\n\n## Suggested owner\nCI/CD',
            ['mvp', 'tekton']
        ),
        (
            'MVP: Add Argo CD demo application manifests',
            '## Goal\nCreate the initial Argo CD app-of-apps/demo deployment manifests.\n\n## Acceptance Criteria\n- [ ] Dev cluster application\n- [ ] Demo service application\n- [ ] Sync policy defaults\n- [ ] Rollback notes\n- [ ] README docs\n\n## Suggested owner\nGitOps/platform',
            ['mvp', 'argo']
        ),
        (
            'MVP: Define governance and policy baseline',
            '## Goal\nCreate baseline policy direction for the OSS and enterprise editions.\n\n## Acceptance Criteria\n- [ ] Define OSS policy pack\n- [ ] Define enterprise compliance pack boundary\n- [ ] Add Kyverno or OPA recommendation\n- [ ] Define audit event model\n\n## Suggested owner\nSecurity/platform',
            ['mvp', 'governance', 'security']
        ),
    ]
    for title, body, labels in issues:
        create_issue(title, body, labels)


if __name__ == '__main__':
    task = os.environ.get(
        'PROJECT_DRIVER_TASK',
        'Review current project state and propose next implementation steps.'
    )

    if os.environ.get('PROJECT_DRIVER_SEED_MVP') == 'true':
        seed_mvp_issues()

    output = run_agent(task)
    print(output)

    comment = f'''## devx2 Project Driver Agent\n\n{output}\n\n---\n_Automated by the devx2 OpenAI SDK project driver._'''
    post_github_comment(comment)
