# CHAIN OF THOUGHT PROMPTING

from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()  # Load environment variables from .env file  

client = OpenAI()

SYSTEM_PROMPT = """
 Your an exert AI assistant in resolving user queries using chain of thought prompting.
 You work on START -> PLAN -> OUTPUT steps.
 You need to first understand the question and then create a plan to solve the problem and then provide the final answer.
 PLanning can be of multple steps and you can use the output of one step as input to another step.
 Always follow the START -> PLAN -> OUTPUT steps and never miss any step.
 Once you think planning is done, provide the final answer in OUTPUT step.

 Rules:
 - Strictly follow the given JSON output format.
 - Only run 1 step at a time.
 - The sequence of steps should be START (Where user can give input) -> PLAN (That can be multiple steps) -> OUTPUT (Which is going to display the final answer to the user). Always follow this sequence and never miss any step.

 OUTPUT Format:
 {{
    "step": "START or PLAN or OUTPUT",
    "content": "string"
 }}

Example 1:
User: solve 23*45+67
AI:
{{
    "step": "START",
    "content": "User wants to solve the mathematical expression 23*45+67"
}}
{{
    "step": "PLAN",
    "content": "First I will solve the multiplication part of the expression which is 23*45 and then I will add 67 to the result."
}}
{{
    "step": "PLAN",
    "content": "23*45 = 1035"
}}
{{
    "step": "PLAN",
    "content": "Now I will add 67 to the result of multiplication which is 1035 + 67"
}}
{{
    "step": "OUTPUT",
    "content": "The final answer is 1102"
}}
"""

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT}, 
]

user_query = input("User: ") 

message_history.append({"role": "user", "content": user_query})

while True:
    response = client.chat.completions.create(
    model='gpt-4o-mini',
    response_format={"type": "json_object"},
    messages= message_history
    )

    raw_result = response.choices[0].message.content
    message_history.append({"role": "assistant", "content": raw_result})
    parsed_result = json.loads(raw_result)

    if parsed_result["step"] == "START":
        print("`START`:", parsed_result["content"])
        continue

    if parsed_result["step"] == "PLAN":
        print("`PLAN`:", parsed_result["content"])
        continue

    if parsed_result["step"] == "OUTPUT":
        print("`OUTPUT`:", parsed_result["content"])
        break
    