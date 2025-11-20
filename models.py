import os
from openai import OpenAI
from openai import AzureOpenAI
import anthropic
import google.generativeai as genai
from decouple import config
# Set OpenAI API KEY
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"
# Set Anthropic API KEY
os.environ['ANTHROPIC_API_KEY'] = "YOUR_ANTHROPIC_API_KEY"
# Set Azure OpenAI API KEY and Endpoint
azure_api_key = "YOUR_AZURE_OPENAI_API_KEY"
# Set NVIDIA API KEY
nvidia_api_key = "YOUR_NVIDIA_API_KEY"
# Set Gemini API KEY
gemini_api_key = "YOUR_GEMINI_API_KEY"

endpoint = os.getenv("ENDPOINT_URL", "YOUR_ENDPOINT_URL")
api_version = "2025-01-01-preview"
client_gpt = OpenAI(
  api_key = os.environ["OPENAI_API_KEY"]
)
client_azure = AzureOpenAI(
    api_key=azure_api_key,
    api_version=api_version,
    azure_endpoint=endpoint,
)


model_init = None
tokenizer = None
def chat(model, messages, temperature=0.1):
    global model_init  
    global tokenizer
    if model == "claude":
        client = anthropic.Anthropic()
        try:
            if any(message.get("role") == "system" for message in messages):
                completion = client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                system=messages[0]["content"],
                messages=messages[1:],
                temperature=temperature,
                max_tokens=1024,
            )
            else:
                completion = client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    messages=messages,
                    temperature=temperature,
                    max_tokens=1024
            )
        except Exception as e:
            import time
            time.sleep(240)
            if any(message.get("role") == "system" for message in messages):
                completion = client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                system=messages[0]["content"],
                messages=messages[1:],
                temperature=temperature,
                max_tokens=1024,
            )
            else:
                completion = client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    messages=messages,
                    temperature=temperature,
                    max_tokens=1024
            )            
        return completion.content[0].text
    elif model == "gpt-4o":
        completion = client_azure.chat.completions.create(
            model="gpt-4o-08-06", 
            messages=messages,
            temperature=temperature
        )
        return completion.choices[0].message.content
    elif model == "gpt-4o-mini":
        completion = client_azure.chat.completions.create(
            model="gpt-4o-mini",  
            messages=messages,
            temperature=temperature
        )
        return completion.choices[0].message.content
    elif model == "llama3.1":
        if model_init is None:
            import mindspore
            from mindnlp.transformers import AutoTokenizer, AutoModelForCausalLM
            model_id = "meta-llama/Llama-3.1-8B-Instruct"
            tokenizer = AutoTokenizer.from_pretrained(model_id)
            tokenizer.pad_token_id = tokenizer.eos_token_id
            model_init = AutoModelForCausalLM.from_pretrained(model_id, ms_dtype=mindspore.bfloat16)
        
        tokenized_chat = tokenizer.apply_chat_template(
            messages, 
            tokenize=True, 
            add_generation_prompt=True, 
            return_tensors="ms"
        )
        
        output = model_init.generate(
            tokenized_chat, 
            max_new_tokens=1024, 
            do_sample=True, 
            temperature=temperature
        )
        input_length = len(tokenized_chat[0])
        generated_tokens = output[0][input_length:]
        return tokenizer.decode(generated_tokens, skip_special_tokens=True) 
    elif model == "Qwen2.5-14B":
        if model_init is None:
            import mindspore
            from mindnlp.transformers import AutoTokenizer, AutoModelForCausalLM
            model_id = "Qwen/Qwen2.5-14B-Instruct"
            tokenizer = AutoTokenizer.from_pretrained(model_id)
            tokenizer.pad_token_id = tokenizer.eos_token_id
            model_init = AutoModelForCausalLM.from_pretrained(model_id, ms_dtype=mindspore.bfloat16)
        
        tokenized_chat = tokenizer.apply_chat_template(
            messages, 
            tokenize=True, 
            add_generation_prompt=True, 
            return_tensors="ms"
        )
        
        output = model_init.generate(
            tokenized_chat, 
            max_new_tokens=1024, 
            do_sample=True, 
            temperature=temperature
        )
        input_length = len(tokenized_chat[0])
        generated_tokens = output[0][input_length:]
        return tokenizer.decode(generated_tokens, skip_special_tokens=True)
    elif model == "gemini":
        genai.configure(api_key=gemini_api_key)
        from google.generativeai.types import HarmCategory, HarmBlockThreshold
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
        generation_config = genai.GenerationConfig(
            max_output_tokens=1024,
            temperature=temperature
        )
        if any(message.get("role") == "system" for message in messages):
            model = genai.GenerativeModel('gemini-2.0-flash-lite-001',system_instruction=messages[0]["content"],safety_settings=safety_settings, generation_config=generation_config)
        else:
            model = genai.GenerativeModel('gemini-2.0-flash-lite-001',safety_settings=safety_settings, generation_config=generation_config)
        for message in messages:
            if message["role"] == "assistant":
                message["role"] = "model"
        if any(message.get("role") == "system" for message in messages):
            messages = messages[1:]
        modify_messages = []
        for message in messages:
            if message["role"] == "user":
                modify_messages.append({'role':'user', 'parts': [{'text': message["content"]}]})
            elif message["role"] == "model":
                modify_messages.append({'role':'model', 'parts': [{'text': message["content"]}]})
        response = model.generate_content(modify_messages)
        return response.text
    elif model == "deepseek_r1":
        try:
            completion = client_gpt.chat.completions.create(
                model="DeepSeek-R1-671B",  
                messages=messages,
                temperature=temperature
            )
            response = completion.choices[0].message.content
            if "</think>" in response:
                response = response.split("</think>")[-1]
            return response
        except Exception as e:
            print(f"error: {str(e)}")
    else:
        raise ValueError(f"Invalid model: {model}")

if __name__ == "__main__":
    test_messages = [
        {"role": "user", "content": "Please introduce yourself."}
    ]
    try:
        response = chat("deepseek_r1", test_messages)
        print("response:")
        print(response)
    except Exception as e:
        print(f"error: {str(e)}")

