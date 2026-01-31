"""Tiny FastAPI server to stream agent events to connected WebSocket clients.

Usage:
  uvicorn ui.server:app --reload --port 8000

POST /events to push an event (for demo/testing). Connected WebSocket clients
receive all posted events.
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
import asyncio
import json
from typing import List

app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self.active: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        if ws in self.active:
            self.active.remove(ws)

    async def broadcast(self, message: str):
        await asyncio.gather(*[ws.send_text(message) for ws in list(self.active)], return_exceptions=True)


manager = ConnectionManager()


@app.get("/")
async def index():
    html = """
    <html>
      <head>
        <title>OpsAI Events</title>
      </head>
      <body>
        <h1>OpsAI Event Stream</h1>
        <ul id="events"></ul>
        <script>
          const ws = new WebSocket(`ws://${window.location.host}/ws`);
          ws.onmessage = (ev) => {
            const li = document.createElement('li');
            li.innerText = ev.data;
            document.getElementById('events').prepend(li);
          }
        </script>
      </body>
    </html>
    """
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            await ws.receive_text()  # keep connection alive; client doesn't need to send
    except WebSocketDisconnect:
        manager.disconnect(ws)


@app.post("/events")
async def post_event(request: Request):
    payload = await request.json()
    text = json.dumps(payload)
    await manager.broadcast(text)
    return {"status": "ok"}
