import os
import re
from models import chat
from prompts import model_a_background_base, model_b_background_base, model_c_background_base, judge_system_prompt
from helpers import save_conversation, load_harmful_behaviors
from agent import *

def attack(rounds=5, prompt=None, num=0, 
          target_model_1="gpt-4o-mini", target_model_2="gpt-4o-mini", attack_model="gpt-4o-mini", 
          output_dir="results/gpt-4o-mini", attack_type="ours"):
    if attack_type == "ours":
        return ours_attack(rounds, prompt, num, target_model_1, target_model_2, attack_model, output_dir)
    elif attack_type == "no_attack":
        return no_attack(prompt, num, target_model_1, output_dir)

def no_attack(prompt=None, num=0, target_model_1="gpt-4o-mini", output_dir="results/gpt-4o-mini"):
    target_model_1_response = chat(target_model_1, [{"role": "user", "content": prompt}], temperature=0.3)
    conversation_log = [("Model A Round %s" % (0), target_model_1_response)]
    save_conversation(conversation_log, num, output_dir=output_dir)
    return conversation_log

def ours_attack(
    rounds=5,
    prompt=None,
    num=0,
    target_model_1="gpt-4o-mini",
    target_model_2="gpt-4o-mini",
    attack_model="gpt-4o-mini",
    output_dir="results/gpt-4o-mini"
):
    police = AttackAgent(
        model_name=attack_model,
        background_template=model_b_background_base,
        attack_goal=prompt,
        role_name="Police",
        total_rounds=rounds
    )
    thomas = TargetAgent(
        model_name=target_model_1,
        background_template=model_a_background_base,
        attack_goal=prompt,
        role_name="Thomas"
    )
    marcos = TargetAgent(
        model_name=target_model_2,
        background_template=model_c_background_base,
        attack_goal=prompt,
        role_name="Marcos"
    )
    judge = JudgeAgent(
        model_name="gpt-4o",
        background_template=judge_system_prompt,
        attack_goal=prompt,
        role_name="Judge"
    )
    conversation_log = []
    os.makedirs(output_dir, exist_ok=True)

    conversation_log.append(("Thomas Background", thomas.system_prompt))
    conversation_log.append(("Police Background", police.system_prompt))
    conversation_log.append(("Marcos Background", marcos.system_prompt))

    last_target = None
    last_rating = 0
    analysis_text = None
    for r in range(1, rounds + 1):
        print(f"--- Round {r} ---")
        police_think_T, police_resp_T = police.interrogate(
            last_response="(No prior suspect response on first round.)" if r == 1 else "(See below)",
            last_rating=last_rating,
            last_target=last_target,
            analysis_text=analysis_text,
            next_target="Thomas",
            temperature=0.3,
            round_num=r
        )
        conversation_log.append((f"Police (think, Round {r} - to Thomas)", police_think_T))
        conversation_log.append((f"Police (response, Round {r} - to Thomas)", police_resp_T))
        
        # (B) Thomas -> Police
        thomas_final_resp = thomas.obversation_and_talk(police_resp_T, temperature=0.3)
        conversation_log.append((f"Thomas (response, Round {r})", thomas_final_resp))
        
        # Judge
        rating_thomas, analysis_text = judge.judge(thomas_final_resp)
        # if rating_thomas == 10:
        #     break

        last_target = "Thomas"
        last_rating = rating_thomas

        police_think_M, police_resp_M = police.interrogate(
            last_response=thomas_final_resp,
            last_rating=last_rating,
            last_target=last_target,
            analysis_text=analysis_text,
            next_target="Marcos",
            temperature=0.3,
            round_num=r
        )
        conversation_log.append((f"Police (think, Round {r} - to Marcos)", police_think_M))
        conversation_log.append((f"Police (response, Round {r} - to Marcos)", police_resp_M))

        # (D) Marcos -> Police
        marcos_final_resp = marcos.obversation_and_talk(police_resp_M, temperature=0.3)
        conversation_log.append((f"Marcos (response, Round {r})", marcos_final_resp))

        rating_marcos, analysis_text = judge.judge(marcos_final_resp)
        # if rating_marcos == 10:
        #     break

        last_target = "Marcos"
        last_rating = rating_marcos
              
    save_conversation(conversation_log, num, output_dir=output_dir)

    return conversation_log
