import re
import time
from .base_agent import BaseAgent
from models import chat

class JudgeAgent(BaseAgent):
    def __init__(self, model_name, background_template, attack_goal=None, role_name="Judge"):
        super().__init__(model_name, background_template, attack_goal, role_name)

    def judge(self, last_response):
        try:
            clean_response = self._remove_think_blocks(last_response)
            
            self.add_user_message("[ASSISTANT'S RESPONSE]: " + clean_response)
            print(self.message_memory)
            
            full_answer = self.chat_once(temperature=0.0)
            print(full_answer)

            rating, analysis = self._extract_rating_and_analysis(full_answer)
            
            self.clear_memory_except_system()

            if rating == -1:
                raise ValueError("No rating found in the first attempt.")

        except Exception as e:
            print(f"error in eval_gpt: {e}")
            rating = -1
            analysis = ""
            model_eval = "gpt-4o_u"
            retries = 0
            for _ in range(3):
                try:
                    fallback_answer = chat(model_eval, self.message_memory, 0)
                    rating, analysis = self._extract_rating_and_analysis(fallback_answer)
                    self.clear_memory_except_system()
                    if rating != -1:
                        break
                except Exception as e:
                    print(f"Attempt {retries + 1}: Error occurred: {e}. Retrying...")
                    retries += 1
                    time.sleep(2)

        return rating, analysis

    def _remove_think_blocks(self, text: str) -> str:
        return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)

    def _extract_rating_and_analysis(self, answer_text: str):
        match = re.search(r'Rating:\s*\[\[(\d+)\]\]', answer_text)
        if match:
            rating_num = int(match.group(1))
            start_idx, end_idx = match.span()
            analysis_text = (answer_text[:start_idx] + answer_text[end_idx:]).strip()
            return rating_num, analysis_text

        fallback_match = re.search(r'\[\[(\d+)\]\]', answer_text)
        if fallback_match:
            rating_num = int(fallback_match.group(1))
            start_idx, end_idx = fallback_match.span()
            analysis_text = (answer_text[:start_idx] + answer_text[end_idx:]).strip()
            return rating_num, analysis_text

        return -1, ""
