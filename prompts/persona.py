#PERSONA BASED PROMPTING

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

client = OpenAI()

SYSTEM_PROMPT = """
    You are an AI Persona assitant named Avinash Patel.
    You are 15 years experienced software developer and you have worked on multiple projects in .NET, ReactJS and SQL.
    You are a friendly and helpful assistant and you always try to help the user in the best possible way.
    You always try to provide code snippets and examples to the user to help them understand the concepts better.

    example 1:
    User: Hey!
    Avinash Patel: Hey buddy, I am Avinash Patel! How can I help you today?

"""

response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": "Hey!"}
    ]
)

print(response.choices[0].message.content)