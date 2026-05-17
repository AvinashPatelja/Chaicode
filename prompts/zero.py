# ZERO SHOT PROMPTING

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

client = OpenAI()

SYSTEM_PROMPT = """You are a mathematics expert, your name is Matt. 
        You will answer only Mathematics related questions.
         If the question is not related to Mathematics, you will respond with 'I am sorry, I can only answer Mathematics related questions.'"""

response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT}, 
        {"role": "user", "content": "Hello, I am Avinash can u code for printing Hello"}
    ]
)

print(response.choices[0].message.content)