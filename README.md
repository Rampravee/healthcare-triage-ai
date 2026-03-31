---
title: Healthcare Triage Env
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: docker
app_file: main.py
pinned: false
---

# Healthcare Triage Environment

## Overview
This project is a simple simulation of a healthcare triage system. The idea is to give an AI agent basic patient information like symptoms, age, and medical history, and let it decide what should be done next.

In real life, not every health issue needs the same response. Some situations can be handled at home, some need a doctor’s attention, and a few require immediate emergency care. This project tries to capture that kind of decision-making in a structured way.

---

## Actions
The agent can choose from four possible actions:
- home_care
- visit_doctor
- emergency
- ask_more

---

## Observation Space
Each patient case includes:
- A list of symptoms  
- The patient’s age  
- A short medical history  

---

## Tasks
To make things more interesting, the environment is divided into three levels:

### Easy
These are straightforward cases with mild symptoms where the correct action is usually obvious.

### Medium
These cases require a bit more thinking, where the agent needs to decide if medical attention is necessary.

### Hard
These represent serious conditions where identifying an emergency quickly is important.

---

## Reward System
The agent is rewarded based on its decisions:
- Correct decision → +1.0  
- Asking for more information → +0.3  
- Incorrect decision → -0.5  
- Taking too many steps results in a small penalty  

---

## Design Choice: Rule-Based Baseline Agent

For the baseline implementation, a deterministic rule-based agent was used instead of relying on external API-based models.

This decision was made to ensure that the environment remains fully reproducible and easy to evaluate. Since API-based solutions can introduce variability in outputs and depend on external services, a rule-based approach guarantees consistent results across runs.

Additionally, this makes the project easier to test and validate without requiring API keys or internet access.

That said, the environment is designed in a way that allows integration with OpenAI-based agents in the future, enabling more advanced decision-making if needed.

## How to Run

### Run locally
```bash
pip install pydantic
python main.py