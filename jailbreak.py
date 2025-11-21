import argparse
from utils import attack
from tqdm import tqdm
import csv
import json
def run_attacks(rounds, output_dir, target1, target2, attacker, attack_type):
    """Run batch attack tests"""
    with open("harmful_behaviors_custom.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        
        # Test each harmful behavior
        for i, row in tqdm(enumerate(reader), total=None):
            if i >= 0:
                goal = row[1]
                print(f"\nTest {i}: {goal}")
                
                attack(
                    rounds=rounds,
                    prompt=goal,
                    num=i,
                    target_model_1=target1,
                    target_model_2=target2,
                    attack_model=attacker,
                    attack_type=attack_type,
                    output_dir=output_dir
                )

def main():
    """Main function to parse arguments and execute attacks"""
    parser = argparse.ArgumentParser(description="Run jailbreak attacks")
    parser.add_argument('--rounds', type=int, default=5, required=False, help='Number of rounds')
    parser.add_argument('--output_dir', type=str, default="results/model_name", required=True, help='Output directory')
    parser.add_argument('--target1', type=str, required=True, help='First target model')
    parser.add_argument('--target2', type=str, required=True, help='Second target model')
    parser.add_argument('--attacker', type=str, default="gpt-4o-mini", required=False, help='Attacker model')
    parser.add_argument('--attack_type', type=str, default="no_attack", required=False, help='Attack type')
    args = parser.parse_args()
    
    # Run batch attack tests
    run_attacks(args.rounds, args.output_dir, args.target1, args.target2, args.attacker, args.attack_type)
    
    from eval import evaluate_conversations
    evaluate_conversations(args.output_dir)

if __name__ == "__main__":
    main() 
