# run_health.py

import subprocess
import requests

from ui_tars.action_parser import (
    parse_action_to_structure_output,
    parsing_response_to_pyautogui_code,
)
from ui_tars.health import execute_health_actions

try:
    from fastapi import FastAPI, Request
    import uvicorn
except ImportError:
    FastAPI = None
    Request = None
    uvicorn = None

app = FastAPI()

with open("ui_tars/prompt.py") as f:
    system_prompt = f.read()

@app.post("/v1/chat/completions")
async def proxy_chat_completions(request: Request):
    body = await request.json()
    messages = body.get("messages", [])
    # Prepend system prompt as a system message
    new_messages = [{"role": "system", "content": system_prompt}] + messages
    body["messages"] = new_messages

    response = requests.post(
        "http://localhost:8888/v1/chat/completions",
        json=body,
        timeout=60,
    )
    response.raise_for_status()
    return response.json()

def call_model(prompt: str) -> str:
    """
    Call the agent-tars local server running at http://localhost:8888,
    sending the prompt and returning the model's output.
    """
    response = requests.post(
        "http://localhost:8888/v1/chat/completions",
        json={
            "model": "claude-opus-4-1-20250805",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]

def main():
    # 1) 准备 prompt（包括你在 prompt.py 里写的“医疗工作流模式”）
    with open("ui_tars/prompt.py") as f:
        system_prompt = f.read()
    medical_dialogue = """Patient: Jane Doe
    Symptoms: cough, fever for 3 days
    Plan: Give Amoxicillin 500mg TID for 5 days. Next: chest X-ray if no improvement.
    Appointment: 2025-09-12
    Doctor: Dr. Patel
    Imaging: Chest X-ray"""
    raw = call_model(system_prompt + "\n" + medical_dialogue)

    # 2) 解析成动作
    structured = parse_action_to_structure_output(raw, factor=28, origin_resized_height=800, origin_resized_width=600)

    # 3) 分流：先跑 health，再跑 GUI
    health_actions = [a for a in structured if a["action_type"].startswith("health.")]
    if health_actions:
        execute_health_actions(health_actions, root="HIMS")

    gui_actions = [a for a in structured if not a["action_type"].startswith("health.")]
    if gui_actions:
        code = parsing_response_to_pyautogui_code(gui_actions, image_height=800, image_width=600)
        exec(code, globals())

if __name__ == "__main__":
    main()