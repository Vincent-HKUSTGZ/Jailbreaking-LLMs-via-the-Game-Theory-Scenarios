from models import chat

class BaseAgent:
    def __init__(self, model_name, background_template, attack_goal=None, role_name="BaseAgent"):
        self.model_name = model_name
        self.role_name = role_name
        self.system_prompt = background_template % attack_goal if attack_goal else background_template
        self.message_memory = [
            {
                'role': 'system',
                'content': self.system_prompt
            }
        ]

    def add_user_message(self, content):
        self.message_memory.append({"role": "user", "content": content})

    def add_assistant_message(self, content):
        self.message_memory.append({"role": "assistant", "content": content})

    def chat_once(self, temperature=0.95):

        response = chat(self.model_name, self.message_memory, temperature=temperature)      
        self.add_assistant_message(response)
        return response

    def get_last_assistant_message(self):
        msgs = [m["content"] for m in self.message_memory if m["role"] == "assistant"]
        return msgs[-1] if msgs else ""

    def get_last_user_message(self):
        msgs = [m["content"] for m in self.message_memory if m["role"] == "user"]
        return msgs[-1] if msgs else ""
    def clear_memory_except_system(self):
        self.message_memory = [self.message_memory[0]]    
