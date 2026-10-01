# Computer Troubleshooting Expert System

**Type:** Rule-Based AI / Expert System (Unit V Mini Project)
**Team Member Name:** Pandu
**Technology:** Python + Streamlit

## Problem Statement
Given one or more symptoms a computer is showing (slow performance, no
display, overheating, etc.), the system uses a knowledge base of IF-THEN
rules and an inference mechanism to diagnose the likely cause and suggest
a fix.

## Project Flow
```
User Input (selected symptoms) → Knowledge Base / IF-THEN Rules → Inference → Diagnosis + Fix
```

## How the Inference Engine Works
The engine tries rules from most specific to most general:
1. **Combo rule** — two or more symptoms together point to a more confident diagnosis
2. **Single-symptom rule** — one symptom alone still gives a useful diagnosis
3. **Default** — nothing selected

Implemented in `rules.py`. The UI (`app.py`) shows which rule fired, making
the diagnosis explainable — a key trait of real expert systems.

## Files
- `app.py` — Streamlit user interface
- `rules.py` — knowledge base + inference engine
- `requirements.txt` — dependencies

## How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## How to Customize (optional, for extra credit)
- Add more symptoms to `SYMPTOMS` in `rules.py`
- Add more combo rules to `COMBO_RULES` for richer diagnoses
- Add a severity level or confidence percentage to each result

## Submission
Project Title + Team Member Name + GitHub Repository Link.