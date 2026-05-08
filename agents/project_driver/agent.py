import os
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
'''


def run_agent(task: str):
    response = client.responses.create(
        model='gpt-5.1',
        input=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': task},
        ],
    )

    return response.output_text


if __name__ == '__main__':
    task = os.environ.get(
        'PROJECT_DRIVER_TASK',
        'Review current project state and propose next implementation steps.'
    )

    print(run_agent(task))
