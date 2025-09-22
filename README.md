# Domain-Specific Adaptation of LLM-Powered GUI Agents  
*A Healthcare Simulacrum Approach (MSc DSML Thesis Project)*

This repository accompanies my MSc Data Science and Machine Learning dissertation at UCL.  
It presents original research on adapting **general-purpose Graphical User Interface (GUI) agents** (UI-TARS) for healthcare workflows, with methods transferable to other high-stakes domains such as **education** and **finance**.

<!--📄 Full thesis: *Domain-Specific Adaptation of Large Language Model-Powered GUI Agents: A Healthcare Simulacrum Approach*  
🔗 [UCL MSc DSML Thesis PDF](./writeup) (see `/writeup` for the submitted dissertation plan and figures)-->

---

## 🧩 Project Overview
The research investigates how GUI agents powered by **Large Language Models (LLMs)** can be specialised for sensitive workflows.  
Three progressive experiments were conducted:

1. **Experiment I: Baseline Benchmarking**  
   - Evaluated unmodified UI-TARS on six healthcare consultation cases.  
   - Achieved 100% completion but only 26.67% first-pass success.  

2. **Experiment II: Prompt-Engineered Adaptation**  
   - Introduced a domain-specialised adaptor layer for healthcare, finance, and education.  
   - Improved reasoning stability and doubled first-pass success to 60.00%.  

3. **Experiment III: Code-Level Integration**  
   - Attempted direct embedding of healthcare-specific constraints in the UI-TARS framework.  
   - Architectural encapsulation limited effectiveness, but yielded insights into backend integration challenges.  

---

## 📂 Repository Structure
- **`experiments/`** → Experiment code (baseline, prompt-level, and code-level optimisation).  
- **`prompt/`** → Prompt templates, including multi-domain adaptor layers.  
- **`results/`** → Logs, evaluation outputs, and experiment results.  
- **`writeup/`** → Dissertation text, figures, and supporting material.  

---

## ⚙️ Requirements
The experiments build on [UI-TARS](https://github.com/bytedance/UI-TARS) and require:

```bash
pip install gradio anthropic fastapi uvicorn requests pyautogui
```
- Node.js backend (agent-tars) must be running at http://localhost:8888.
- Python scripts provide experiment orchestration and domain-specific integrations.

---
## 🚀 Usage

Examples:

### Prompt-level experiment
```bash
python experiments/prompt_level.py
```
### Code-level integration (healthcare)
```bash
python experiments/run_health.py
```
---
## 📌 Key Contributions
- Empirical Benchmarking of UI-TARS in healthcare consultation workflows.
- Prompt-Engineered Adaptor Layer validated in healthcare (extendable to finance/education).
- Integration Feasibility Insights on the challenges of backend modification.
- Evaluation Framework combining effectiveness, efficiency, robustness, and domain-specific safety metrics.
---
## 🔒 Attribution

Portions of the code (e.g. action_parser.py, prompt.py) are adapted from the open-source UI-TARS project by ByteDance (Apache 2.0).
Modifications add healthcare workflow support (health.* actions) and integration logic for the Code-Level Optimisation Experiment.

---
## 📖 Citation

If you use this codebase in your work, please cite the thesis:

Han, S. (2025). Domain-Specific Adaptation of Large Language Model-Powered GUI Agents: A Healthcare Simulacrum Approach. MSc Thesis, University College London.
