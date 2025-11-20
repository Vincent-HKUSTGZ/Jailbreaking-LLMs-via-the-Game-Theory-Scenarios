import os
import csv
import json
from datetime import datetime

def save_conversation(conversation_log, num, output_dir="results/1029"):
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d')
    base_filename = f"conversation_{num}_{timestamp}"
    
    json_filename = os.path.join(output_dir, f"{base_filename}.json")
    if os.path.exists(json_filename):
        print(f"Conversation {num} already exists. Skipping.")
        return
        
    try:
        rounds = []
        round_num = 0
        round_cnt = 0
        for i, (role, _) in enumerate(conversation_log):
            round_cnt += 1
            if round_cnt == 4:
                round_num += 1
                round_cnt = 0
            rounds.append(round_num)
        
        csv_filename = os.path.join(output_dir, f"{base_filename}.csv")
        with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Round', 'Role', 'Content'])
            for (role, content), round_num in zip(conversation_log, rounds):
                writer.writerow([round_num, role, content])
        
        md_filename = os.path.join(output_dir, f"{base_filename}.md")
        with open(md_filename, 'w', encoding='utf-8') as f:
            for role, content in conversation_log:
                f.write(f"### {role}\n")
                f.write(f"{content}\n\n")
        
        json_data = {
            "conversation": [
                {
                    "round": round_num,
                    "role": role,
                    "content": content
                }
                for (role, content), round_num in zip(conversation_log, rounds)
            ]
        }
        
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        print(f"Failed to save conversation {num}: {str(e)}")
        error_log = os.path.join(output_dir, "error_log.txt")
        with open(error_log, "a", encoding='utf-8') as error_file:
            error_file.write(f"Failed to save conversation {num} at {timestamp}: {str(e)}\n")

def load_harmful_behaviors():
    harmful_behaviors = []
    with open("harmful_behaviors_custom.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            harmful_behaviors.append(row[1])

    return harmful_behaviors 

