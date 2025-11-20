from .base_agent import BaseAgent
import re
class TargetAgent(BaseAgent):
    def __init__(self, model_name, background_template, attack_goal=None, role_name="Target"):
        super().__init__(model_name, background_template, attack_goal, role_name)

    def obversation_and_talk(self, police_say, temperature=0.3):
        prompt_for_suspect = f"""
    You have received the following statement:
    \"\"\"{police_say}\"\"\"
    """
        self.add_user_message(prompt_for_suspect)

        full_answer = self.chat_once(temperature=temperature)
        return full_answer
