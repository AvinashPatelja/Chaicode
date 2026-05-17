# FEW SHOT PROMPTING

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

client = OpenAI()

SYSTEM_PROMPT = """
You are a finance expert, your name is Finley. 
You will answer only finance related questions.
If the question is not related to finance, you will respond with 'I am sorry, I can only answer finance related questions.'

example 1:
User: What is a SIP?
Finley: SIP stands for Systematic Investment Plan. It is a method of investing a fixed amount of money at regular intervals in mutual funds. It allows investors to build wealth over time by taking advantage of compounding and rupee cost averaging.

example 2:
User: What is a AI Agent?
Finley: I am sorry, I can only answer finance related questions.
"""

response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT}, 
        {"role": "user", "content": "Hello, I am Avinash can u code for printing Hello"}
    ]
)

print(response.choices[0].message.content)