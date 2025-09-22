# Prompt-Level Optimisation Experiment

This folder contains **`prompt_level.py`**, an experiment exploring prompt-level interventions for large language model (LLM) agents. The goal is to test how domain-specific system prompts and optimisation frameworks can improve prompt quality across different application areas.

---

## 🧩 What this experiment does
- Provides **scene-specific system prompts** for domains:
  - Healthcare
  - Education
  - Finance
- Implements a **Prompt Optimizer** class that:
  - Takes an input prompt
  - Optimises it using Anthropic Claude models
  - Returns both an optimised version and an explanation of improvements
- Runs through a **Gradio web interface** for interactive use
- Supports **streaming responses** and **chat history management**

---

## ⚙️ Requirements
Install dependencies:
```bash
pip install gradio anthropic
```
---

## 🚀 Usage
1.	Export your Anthropic API key:
```bash
export ANTHROPIC_API_KEY="your_api_key_here"
```

2.	Run the experiment:
```bash
python prompt_level.py
```
3.	Open the Gradio interface in your browser:
👉 http://127.0.0.1:7860

You can then enter prompts, select a domain scene, and view optimised results with explanations.

---

## 📂 Structure
- prompt_level.py – main script for this experiment
  - Scene System Prompts: predefined domain-specific contexts
  - PromptOptimizer class: core logic for prompt improvement
  - Gradio UI: frontend for user interaction
 


# Code-Level Optimisation Experiment


This experiment explores **code-level integration** of domain-specific functionality into the `UI-TARS` agent framework.  
Unlike prompt-only interventions, this layer modifies the backend logic to embed healthcare workflows and structured action execution directly into the system.

---

## Attribution

Portions of this experiment adapt code from the open-source [UI-TARS](https://github.com/bytedance/UI-TARS) project by ByteDance (Apache 2.0 licensed).  
Modifications include healthcare workflow support (`health.*` actions) and integration logic for the Code-Level Optimisation Experiment.

---

## 🧩 Overview
The code in this folder enables:
- Parsing **model outputs** into structured actions  
- Executing **healthcare-specific workflows** (appointments, imaging, treatment plans)  
- Bridging between **LLM reasoning traces** and **OS-level GUI actions**

This represents an attempt at **native integration**, where constraints and reasoning patterns are enforced directly at the code level.

---

## 📂 Structure

### `health.py` (new in this experiment)
- Defines a lightweight **`DialogueInfo` dataclass** for storing structured patient data.  
- Implements **heuristic extractors** from raw dialogue text:
  - Patient name, symptoms, treatment plan, appointment, doctor, imaging.  
- Provides **filesystem helpers** (`/HIMS` directory):
  - Organises patient folders, demographics, symptoms, treatment plans, appointments, and imaging plans.  
- Includes **`execute_health_actions()`**, an entrypoint that executes health-specific actions such as:
  - `health.extract_and_update`
  - `health.ensure_hims`
  - `health.upsert_patient`

---

### `action_parser.py` (adapted from [UI-TARS](https://github.com/bytedance/UI-TARS))
- Originally developed in the **UI-TARS** repository.  
- Parses **LLM-generated action strings** into Python objects.  
- Key functions:
  - `parse_action_to_structure_output()` → Converts reasoning traces into structured `action_type` and `action_inputs`.  
  - `parsing_response_to_pyautogui_code()` → Translates GUI actions into executable **PyAutoGUI** code.  
- Includes resizing utilities (`smart_resize`, `linear_resize`) for handling screenshots in GUI tasks.  
- Supports a wide action space (click, drag, type, scroll, hotkey, etc.), mapping them into code for automation.

---

### `prompt.py` (adapted from [UI-TARS](https://github.com/bytedance/UI-TARS))
- Contains **system prompts** that guide the agent:
  - **`COMPUTER_USE_DOUBAO`** → Desktop GUI workflows (click, drag, type, screenshot, health.* actions).  
  - **`MOBILE_USE_DOUBAO`** → Mobile GUI workflows (tap, long press, open app, back/home navigation).  
  - **`GROUNDING_DOUBAO`** → Minimal grounding prompt for simplified action parsing.  
- The **Healthcare Workflow Mode** section (added in this experiment) specifies that when hospital information management system (HIMS) dialogue appears, the agent should output `health.*` actions **instead of GUI keystrokes**.

---

### `run_health.py` (integration script)
- Provides a runnable entrypoint that ties everything together.  
- Steps:
  1. Loads the **system prompt** (with medical workflow rules).  
  2. Sends dialogue + system prompt to the model (via local agent-tars server).  
  3. Parses the model output into structured actions.  
  4. Splits execution:
     - **Healthcare actions** → stored into `/HIMS` patient management files.  
     - **GUI actions** → executed with **PyAutoGUI** for automation.  
- Also exposes a **FastAPI proxy endpoint** (`/v1/chat/completions`) that injects the system prompt automatically.

---

## ⚙️ Requirements
Install dependencies:
```bash
pip install fastapi uvicorn requests pyautogui
```
You also need:
	•	A running agent-tars server at http://localhost:8888/v1/chat/completions.
	•	Write access to the working directory for /HIMS patient records.

 ## 🚀 Usage
1.	Start the agent-tars backend:
```bash
cd agent-tars
npm run start
```
2.	Run the healthcare experiment:
```bash
 python experiments/run_health.py
```
3.	Check the /HIMS directory:
- Patients/ → demographics, symptoms, treatment plans
- Appointments/appointments.txt
- Imaging/imaging_plan.txt
