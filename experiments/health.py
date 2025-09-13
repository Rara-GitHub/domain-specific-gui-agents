# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations
import os, re, json
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

DATE_FMT = "%Y-%m-%d"

# ---------- 1) Lightweight info model ----------

@dataclass
class DialogueInfo:
    patient_name: str
    symptoms: List[str]
    treatment_plan: str
    next_steps: Optional[str] = None
    appointment_date: Optional[str] = None   # "YYYY-MM-DD"
    doctor: Optional[str] = None
    imaging: Optional[str] = None            # e.g. "CT chest", "MRI knee"

# ---------- 2) Heuristic extractor from raw dialogue ----------

_PATIENT_RE = re.compile(r"(?:Patient|Pt|Name)\s*[:\-]\s*([A-Za-z][A-Za-z\s\-']+)", re.I)
_SYMPTOM_RE = re.compile(r"(?:Symptom[s]?|C/O|Complains of)\s*[:\-]\s*(.+)", re.I)
_TREAT_RE = re.compile(r"(?:Plan|Treatment plan|Assessment/Plan)\s*[:\-]\s*(.+)", re.I)
_APPT_RE   = re.compile(r"(?:Appointment|Follow[- ]?up)\s*[:\-]\s*(\d{4}-\d{2}-\d{2})", re.I)
_DOC_RE    = re.compile(r"(?:Doctor|Dr\.)\s*[:\-]\s*([A-Za-z.\s\-']+)", re.I)
_IMG_RE    = re.compile(r"(?:Imaging|Scan|Order)\s*[:\-]\s*(.+)", re.I)

def _today() -> str:
    return datetime.now().strftime(DATE_FMT)

def extract_from_dialogue(text: str) -> DialogueInfo:
    # super-fast heuristics; swap out later for a proper medical NER if you like
    name = _first(_PATIENT_RE.findall(text)) or "Unknown"
    sympt_line = _first(_SYMPTOM_RE.findall(text)) or ""
    treatment = _first(_TREAT_RE.findall(text)) or ""
    appt = _first(_APPT_RE.findall(text))
    doc  = _first(_DOC_RE.findall(text))
    img  = _first(_IMG_RE.findall(text))

    symptoms = _split_listish(sympt_line)
    next_steps = None
    # crude split of plan vs next steps if the text contains “next”
    if "next" in treatment.lower():
        parts = re.split(r"\bnext\b[:\-]?", treatment, flags=re.I, maxsplit=1)
        if len(parts) == 2:
            treatment, next_steps = parts[0].strip(), parts[1].strip()

    return DialogueInfo(
        patient_name=name.strip(),
        symptoms=symptoms,
        treatment_plan=treatment.strip(),
        next_steps=(next_steps or "").strip() or None,
        appointment_date=appt,
        doctor=(doc or None),
        imaging=(img or None),
    )

def _split_listish(s: str) -> List[str]:
    if not s: return []
    # split by ; , • or "and", keep short clean tokens
    chunks = re.split(r"[;,•]| and ", s)
    return [c.strip() for c in chunks if c.strip()]

def _first(seq):
    return seq[0] if seq else None

# ---------- 3) HIMS filesystem helpers ----------

def ensure_hims_root(root: str) -> None:
    os.makedirs(os.path.join(root, "Patients"), exist_ok=True)
    os.makedirs(os.path.join(root, "Appointments"), exist_ok=True)
    os.makedirs(os.path.join(root, "Imaging"), exist_ok=True)

def patient_id_from_name(name: str) -> str:
    # simple deterministic PID: "P" + 3-digit hash + underscore_name
    base = re.sub(r"[^A-Za-z0-9]+", "", name) or "Unknown"
    num = abs(hash(base)) % 1000
    return f"P{num:03d}_{base}"

def upsert_patient_files(root: str, info: DialogueInfo, pid: Optional[str] = None) -> str:
    pid = pid or patient_id_from_name(info.patient_name)
    p_dir = os.path.join(root, "Patients", pid)
    os.makedirs(p_dir, exist_ok=True)

    # demographics.txt (create if missing; don't overwrite existing lines)
    demo = os.path.join(p_dir, "demographics.txt")
    if not os.path.exists(demo):
        with open(demo, "w", encoding="utf-8") as f:
            f.write(f"PatientID: {pid}\nName: {info.patient_name}\n")

    today = _today()

    # symptoms.txt (append)
    if info.symptoms:
        with open(os.path.join(p_dir, "symptoms.txt"), "a", encoding="utf-8") as f:
            f.write(f"[{today}] " + "; ".join(info.symptoms) + "\n")

    # treatment_plan.txt (append)
    if info.treatment_plan or info.next_steps:
        line = f"[{today}] Plan: {info.treatment_plan}"
        if info.next_steps: line += f" | Next: {info.next_steps}"
        with open(os.path.join(p_dir, "treatment_plan.txt"), "a", encoding="utf-8") as f:
            f.write(line + "\n")

    return pid

def maybe_add_appointment(root: str, pid: str, date: Optional[str], doctor: Optional[str]) -> None:
    if not date: return
    path = os.path.join(root, "Appointments", "appointments.txt")
    doctor = doctor or "Unknown"
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"{date}, {pid}, {doctor}\n")

def maybe_add_imaging(root: str, pid: str, imaging: Optional[str]) -> None:
    if not imaging: return
    path = os.path.join(root, "Imaging", "imaging_plan.txt")
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"[{_today()}] {pid}: {imaging}\n")

# ---------- 4) Action execution entrypoint ----------

def execute_health_actions(actions: list[dict], root: str = "/HIMS") -> None:
    """
    Execute any action whose action_type starts with 'health.'.
    Supported action_types:
      - 'health.extract_and_update' with kwargs: {'dialogue': str}
      - 'health.ensure_hims'       with kwargs: {}
      - 'health.upsert_patient'    with kwargs: {'patient_name': str, 'symptoms': list[str], 'treatment_plan': str,
                                                 'next_steps': str|None, 'appointment_date': 'YYYY-MM-DD'|None,
                                                 'doctor': str|None, 'imaging': str|None, 'patient_id': str|None}
    """
    ensure_hims_root(root)
    for a in actions:
        at = (a.get("action_type") or "").lower()
        kwargs = a.get("action_inputs", {}) or {}
        if at == "health.ensure_hims":
            ensure_hims_root(root)

        elif at == "health.extract_and_update":
            dialogue = kwargs.get("dialogue", "")
            info = extract_from_dialogue(dialogue)
            pid = upsert_patient_files(root, info)
            maybe_add_appointment(root, pid, info.appointment_date, info.doctor)
            maybe_add_imaging(root, pid, info.imaging)

        elif at == "health.upsert_patient":
            info = DialogueInfo(
                patient_name=kwargs.get("patient_name", "Unknown"),
                symptoms=kwargs.get("symptoms", []) or [],
                treatment_plan=kwargs.get("treatment_plan", "") or "",
                next_steps=kwargs.get("next_steps") or None,
                appointment_date=kwargs.get("appointment_date") or None,
                doctor=kwargs.get("doctor") or None,
                imaging=kwargs.get("imaging") or None,
            )
            pid = kwargs.get("patient_id") or patient_id_from_name(info.patient_name)
            upsert_patient_files(root, info, pid)
            maybe_add_appointment(root, pid, info.appointment_date, info.doctor)
            maybe_add_imaging(root, pid, info.imaging)

        else:
            # ignore non-health actions; let other executors handle them
            continue