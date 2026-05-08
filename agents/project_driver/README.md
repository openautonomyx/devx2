# devx2 Project Driver Agent

OpenAI SDK-based autonomous project orchestration agent for devx2.

## Responsibilities

- roadmap planning
- implementation decomposition
- architecture guidance
- GitHub issue planning
- sprint recommendations
- platform engineering guidance
- GTM artifact drafting

## Environment Variables

```bash
OPENAI_API_KEY=
GITHUB_TOKEN=
PROJECT_DRIVER_TASK=
```

## Run locally

```bash
pip install -r requirements.txt
python agent.py
```

## GitHub Automation

The GitHub Action runs on:

- issue events
- pull request events
- manual dispatch

## Future roadmap

- GitHub issue auto-creation
- milestone orchestration
- PR reviews
- architecture linting
- Backstage integration
- Argo/Tekton workflow awareness
- multi-agent orchestration
- memory/state store
