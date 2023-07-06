#create engine for AI model
import openai
import os
from dotenv import load_dotenv

load_dotenv('.env')

openai.api_key = os.getenv("OPENAI")

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI")

def set_open_params(
    model="text-davinci-003",
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
):
  
    openai_params = {}    

    openai_params['model'] = model
    openai_params['temperature'] = temperature
    openai_params['max_tokens'] = max_tokens
    openai_params['top_p'] = top_p
    openai_params['frequency_penalty'] = frequency_penalty
    openai_params['presence_penalty'] = presence_penalty
    return openai_params

def get_completion(params, prompt):

    response = ai.Completion.create(
        engine = params['model'],
        prompt = prompt,
        temperature = params['temperature'],
        max_tokens = params['max_tokens'],
        top_p = params['top_p'],
        frequency_penalty = params['frequency_penalty'],
        presence_penalty = params['presence_penalty'],
    )
    return response

def gpt_turbo(prompt):
    return openai.ChatCompletion.create(
            model = 'gpt-3.5-turbo',
            #model='text-davinci-003',
            messages = [
                {'role'  : 'user', 
                'content':  prompt}
            ],
            temperature = 0.2
            )

def gpt(prompt, model):
    return openai.ChatCompletion.create(
            model = model,
            messages = [
                {'role'  : 'user', 
                'content':  prompt}
            ],
            temperature = 0.2
            )

