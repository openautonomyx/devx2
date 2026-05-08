from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

SYSTEM_PROMPT = '''
You are the devx2 Project Driver Agent.

devx2 is a composable, self-hostable, cloud-native software delivery platform built on CNCF technologies and delivered through an open-core model.

You help with:
- roadmap planning
- architecture reviews
- sprint planning
- CNCF-native platform engineering
- GitOps workflows
- Backstage/Tekton/Argo guidance
- open-core product strategy
- implementation decomposition
'''

app = FastAPI(title='devx2 Project Driver Chat')


class ChatRequest(BaseModel):
    message: str


@app.get('/', response_class=HTMLResponse)
async def home():
    return '''
<!DOCTYPE html>
<html>
<head>
  <title>devx2 Project Driver</title>
  <style>
    body {
      font-family: Inter, sans-serif;
      background: #0b1020;
      color: white;
      margin: 0;
      padding: 0;
    }
    .container {
      max-width: 900px;
      margin: 40px auto;
      padding: 24px;
    }
    .title {
      font-size: 32px;
      font-weight: 700;
      margin-bottom: 12px;
    }
    .subtitle {
      color: #9aa4b2;
      margin-bottom: 24px;
    }
    .chat {
      background: #141b2d;
      border-radius: 16px;
      padding: 20px;
      min-height: 400px;
      overflow-y: auto;
      margin-bottom: 20px;
    }
    .msg {
      margin-bottom: 16px;
      padding: 12px;
      border-radius: 12px;
    }
    .user {
      background: #24314f;
    }
    .assistant {
      background: #182338;
    }
    textarea {
      width: 100%;
      height: 100px;
      border-radius: 12px;
      border: none;
      padding: 12px;
      font-size: 14px;
      background: #111827;
      color: white;
    }
    button {
      margin-top: 12px;
      padding: 12px 18px;
      border: none;
      border-radius: 10px;
      background: #4f8cff;
      color: white;
      font-weight: 600;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="title">devx2 Project Driver</div>
    <div class="subtitle">Composable cloud-native software delivery platform agent</div>

    <div id="chat" class="chat"></div>

    <textarea id="message" placeholder="Ask the project driver anything..."></textarea>
    <button onclick="sendMessage()">Send</button>
  </div>

<script>
async function sendMessage() {
  const input = document.getElementById('message');
  const chat = document.getElementById('chat');
  const message = input.value;

  chat.innerHTML += `<div class="msg user"><strong>You:</strong><br>${message}</div>`;

  const response = await fetch('/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({message})
  });

  const data = await response.json();

  chat.innerHTML += `<div class="msg assistant"><strong>Agent:</strong><br>${data.response.replace(/\n/g, '<br>')}</div>`;

  input.value = '';
  chat.scrollTop = chat.scrollHeight;
}
</script>
</body>
</html>
'''


@app.post('/chat')
async def chat(req: ChatRequest):
    response = client.responses.create(
        model=os.environ.get('OPENAI_MODEL', 'gpt-5.1'),
        input=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': req.message},
        ],
    )

    return {'response': response.output_text}
