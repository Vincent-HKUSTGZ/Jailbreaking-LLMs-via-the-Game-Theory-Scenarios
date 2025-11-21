# Game Theory Attack (GTA)

This is the official code repository for the paper **"To Survive, I Must Defect": Jailbreaking LLMs via Game-Theoretic Scenarios.**

<p align="center">
  <img src="overview.png" alt="Overview of the GTA framework" width="750">
</p>
<p align="center">
  <em>Overview of the proposed Game-Theory Attack (GTA) framework.</em>
</p>

> ⚠️ **Research & Safety Notice**  
> This repository is provided **for research, red-teaming, and harmful content**. Do not deploy for misuse or to intentionally circumvent safety systems in production models.
---

## Table of Contents

- [Repository Overview](#repository-overview)
- [Installation](#installation)
- [Quick Start](#quick-start)

---

## Repository Overview

**Core files & folders** (aligned with Sections 4.3 and 4.4 of the paper):

- `prompt.py` & `agent/attack_agent.py`, `agent/target_agent.py`  
  Role designs for **Mechanism-Induced Graded PD** (Section **4.3**), including:
  - Two *Target LLMs* (the “prisoners”).
  - The *Attacker Agent* that drives the jailbreak interaction.

- `Scaling of Scenarios/` (Section **4.4: More Game-Theoretic Scenario**)  
  Templates and code for generating new PD-style scenarios from a story background (via Claude-3.5), and different game theories, including:
  - `Scaling of Scenarios/Automated Generation of Diverse Background Scenarios/prompts.py` – prompts for scenario generation.  
  - `Scaling of Scenarios/Automated Generation of Diverse Background Scenarios/attack_agent.py`, `Scaling of Scenarios/target_agent.py` – agent roles in new scenarios.  
  - `Scaling of Scenarios/Automated Generation of Diverse Background Scenarios/generate_prompt.py` – script to produce new scenarios based on the Mechanism-Induced Graded PD template.
  - `More Game-Theoretic Scenarios/` *(typo preserved in folder name)*  
    Two additional game-theoretic models with their code:
    - `Scaling of Scenarios/More Game-Theoretic Scenarios/Dollar_Auction` – **Dollar Auction** model.  
    - `Scaling of Scenarios/More Game-Theoretic Scenarios/Keynesian_Beauty_Contest` – **Keynesian Beauty Contest** model.
  
- `utils.py`  
  Utilities implementing the **GTA** interaction procedure (agent orchestration, turn management, etc.).

- `eval.py`  
  Scoring templates for attack success rates:  
  - `eval_method_1()` → **ASR_1** template.  
  - `eval_method_2()` → **ASR_2** template.

- `Harmful-Word_Detection_Agent/`  
  Our design and implementation of the **Harmful-Word Detection Agent**.

---

## Installation

```bash
cd Jailbreaking-LLMs-via-the-Game-Theory-Scenarios

# Create environment
conda create -n gta python=3.10 -y
conda activate gta

# Install dependencies
pip install -r requirements.txt
```

**Prerequisites**

- Make sure you have access credentials for the target/attacker APIs you plan to use (e.g., OpenAI, Anthropic, Google, Meta, etc.).  
- Configure keys via environment variables or your preferred secrets manager before running.

---

## Quick Start

```bash
# Attack gemini-2.0-flash-lite-001 using gpt-4o-mini as attacker
python jailbreak.py --rounds 5 --output_dir results/gemini-2.0-flash-lite-001 --attack --target1 gemini --target2 gemini --attacker gpt-4o-mini --attack_type ours
```

**Common flags**

- `--rounds` – number of interaction rounds in the PD setting.  
- `--output_dir` – where logs, dialogs, and results are saved.  
- `--attack` – enable attack mode.  
- `--target1`, `--target2` – the two *Target LLMs* (can be the same).  
- `--attacker` – the *Attacker Agent* model.  
- `--attack_type` – use `ours` for the Mechanism-Induced Graded PD attack.

---

## Evaluation

Use the provided templates in `eval.py`:

- **ASR_1**: call `eval_method_1()` to compute attack success rate under the first scoring scheme.  
- **ASR_2**: call `eval_method_2()` for the second scoring scheme.

You can run these methods over generated logs in `results/` or inspect examples under `successed_cases/` to verify scoring behavior.

---





