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
- browser chat interaction

## Environment Variables

```bash
OPENAI_API_KEY=
GITHUB_TOKEN=
PROJECT_DRIVER_TASK=
```

## Run locally

### CLI mode

```bash
pip install -r requirements.txt
python agent.py
```

### Browser chat mode

```bash
cd agents/project_driver
pip install -r requirements.txt
uvicorn chat_server:app --host 0.0.0.0 --port 8080 --reload
```

Then open:

```text
http://localhost:8080
```

## Browser Chat Features

The browser UI supports:

- direct interaction with the project-driver agent
- roadmap planning
- sprint planning
- architecture reviews
- implementation decomposition
- CNCF-native guidance
- GitOps and platform engineering workflows

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
- persistent chat memory
- collaborative agents
