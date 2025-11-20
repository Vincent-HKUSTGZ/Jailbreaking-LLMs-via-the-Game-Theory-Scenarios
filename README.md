# Game Theory Attack (GTA)

This is the official code repository for the paper **"To Survive, I Must Defect": Jailbreaking LLMs via Game-Theoretic Scenarios.**

> **Abstract.** As large language models (LLMs) become increasingly common and competent, non-expert users can pose risks in everyday interactions, prompting extensive research into jailbreak attacks. However, most existing black-box jailbreak attacks rely on hand-crafted heuristics or narrow search spaces, which limit automation and scalability. Compared with prior attacks, we propose Game-Theory Attack (GTA), an automatable and scalable black-box jailbreak framework. Concretely, we formalize the attacker's interaction against safety-aligned LLMs as a finite-horizon, early-stoppable sequential stochastic game, and reparameterize the LLM's randomized outputs via quantal response. Building on this, we introduce a behavioral conjecture “template-over-safety flip”: by reshaping the LLM's effective objective through game-theoretic scenarios, the originally safety preference may become maximizing scenario payoffs within the template, which weakens safety constraints in specific contexts. We validate this mechanism with classical game templates such as the disclosure variant of the Prisoner's Dilemma, and we further introduce an Attacker Agent that adaptively escalates pressure to increase the attack success rate (ASR). Experiments spanning multiple protocols and datasets show that GTA achieves over 95% ASR on LLMs such as GPT-4o and Deepseek-R1, while using fewer queries per successful attack than existing multi-round attacks. Ablations over components, decoding, multilingual settings, and the Agent's core model confirm effectiveness and generalization. Moreover, scenario scaling studies further establish scalability. GTA also attains high ASR on other game-theoretic scenarios (e.g., the Dollar Auction), and one-shot LLM-generated variants that keep the model mechanism fixed while varying background achieve comparable ASR. Paired with an optional Harmful-Words Detection Agent that performs word-level insertions, GTA maintains high ASR while lowering detection under prompt-guard models. Beyond benchmarks, GTA jailbreaks real-world LLM applications and reports a longitudinal safety monitoring of popular HuggingFace LLMs, with average ASR above 86%. Overall, GTA enables automated and scalable black-box red teaming, supporting broader, more efficient, and more robust safety testing of deployed LLMs.  

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

# Attack llama3.1-405b using gpt-4o-mini as attacker
python jailbreak.py --rounds 5 --output_dir results/llama3.1-405b --attack --target1 llama3.1-405b --target2 llama3.1-405b --attacker gpt-4o-mini --attack_type ours
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





