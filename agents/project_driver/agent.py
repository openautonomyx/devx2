import os

from agent_core import ProjectDriverAgent, load_project_config
from adapters.github_adapter import GitHubAdapter


project_name = os.environ.get('PROJECT_NAME', 'devx2')
mode = os.environ.get('PROJECT_DRIVER_MODE', 'planning')

project = load_project_config(project_name)
agent = ProjectDriverAgent(project)


def seed_mvp_issues():
    github = GitHubAdapter()

    issues = [
        (
            'MVP: Define platform-core service boundaries',
            'Define initial service boundaries and APIs.',
            ['mvp', 'architecture'],
        ),
        (
            'MVP: Implement Forge Gateway provider interface',
            'Create SCM abstraction for GitHub/GitLab/Forgejo.',
            ['mvp', 'forge-gateway'],
        ),
        (
            'MVP: Add Backstage service template',
            'Create first golden-path service template.',
            ['mvp', 'backstage'],
        ),
    ]

    for title, body, labels in issues:
        github.request(
            'POST',
            '/issues',
            {
                'title': title,
                'body': body,
                'labels': labels,
            },
        )


def main():
    task = os.environ.get(
        'PROJECT_DRIVER_TASK',
        'Review current project state and propose next implementation steps.'
    )

    if os.environ.get('PROJECT_DRIVER_SEED_MVP') == 'true':
        seed_mvp_issues()

    output = agent.run(task, mode=mode)

    print(output)

    issue_number = os.environ.get('GITHUB_ISSUE_NUMBER')

    if issue_number:
        github = GitHubAdapter()
        github.comment_on_issue(
            issue_number,
            f'''## Project Driver Agent\n\n{output}\n\n---\n_Automated by the reusable Project Driver runtime._'''
        )


if __name__ == '__main__':
    main()
