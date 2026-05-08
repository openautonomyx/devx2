from openai import OpenAI
import os


class ProjectDriverAgent:
    def __init__(self, project_config: dict):
        self.project = project_config
        self.client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

    def build_system_prompt(self) -> str:
        return f'''
You are a reusable Project Driver Agent.

Project name:
{self.project['name']}

Project category:
{self.project['category']}

Positioning:
{self.project['positioning']}

Architecture:
{', '.join(self.project['architecture'])}

Principles:
{', '.join(self.project['principles'])}

Responsibilities:
{', '.join(self.project['responsibilities'])}

Your job is to help drive software delivery, architecture planning,
roadmaps, sprint planning, implementation decomposition, governance,
and platform engineering decisions.

Be concise, structured, and actionable.
'''

    def run(self, task: str, mode: str = 'planning') -> str:
        response = self.client.responses.create(
            model=os.environ.get('OPENAI_MODEL', 'gpt-5.1'),
            input=[
                {
                    'role': 'system',
                    'content': self.build_system_prompt(),
                },
                {
                    'role': 'user',
                    'content': f'Mode: {mode}\n\nTask:\n{task}',
                },
            ],
        )

        return response.output_text
