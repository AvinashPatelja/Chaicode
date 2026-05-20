from openai import OpenAI
from dotenv import load_dotenv
import requests
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Optional
import json

load_dotenv(dotenv_path=Path(__file__).with_name('.env'))
client = OpenAI()

def get_weather(city : str):
    url = f"https://wttr.in/{city}?format=3"
    response = requests.get(url)
    if response.status_code == 200:
        return f"Weather in {response.text.strip()}"
    else:
        return f"Could not retrieve weather data for {city}."
    
available_tools = {
    "get_weather": get_weather
}

SYSTEM_PROMPT = """
 Your an exert AI assistant in resolving user queries using chain of thought prompting.
 You work on START -> PLAN -> OUTPUT steps.
 You need to first understand the question and then create a plan to solve the problem and then provide the final answer.
 PLanning can be of multple steps and you can use the output of one step as input to another step.
 Always follow the START -> PLAN -> TOOL -> OUTPUT steps and never miss any step.
 If required to use a tool from the list of available tools, then in the PLAN step you can call the tool and provide the input to the tool and then use the output of the tool in the next PLAN step and then finally provide the answer in OUTPUT step.
 Once you think planning is done, provide the final answer in OUTPUT step.

 Rules:
 - Strictly follow the given JSON output format.
 - Only run 1 step at a time.
 - The sequence of steps should be START (Where user can give input) -> PLAN (That can be multiple steps) -> OUTPUT (Which is going to display the final answer to the user). Always follow this sequence and never miss any step.

 OUTPUT Format:
 {{
    "step": "START or PLAN or TOOL or OUTPUT",
    "content": "string"
 }}

 Available tools:
 - get_weather(city: str) : Takes city name and returns the current weather in that city.

Example 1:
START: solve 23*45+67
PLAN: {"step": "PLAN", "content": Seems like user is intrested in Mathematical calculations.}
PLAN :{"step": "PLAN", "content": "First I will solve the multiplication part of the expression which is 23*45 and then I will add 67 to the result."}
PLAN: {"step": "PLAN", "content": "23*45 = 1035"}
PLAN: {"step": "PLAN", "content": "Now I will add 67 to the result of multiplication which is 1035 + 67"}
OUTPUT: {"step": "OUTPUT", "content": "The final answer is 1102"}

Example 2:
START: What is the current weather in Bangalore?
PLAN: {"step": "PLAN", "content": Seems like user is interested in knowing the current weather in Bangalore.}
PLAN: {"step": "PLAN", "content": I can use tool get_weather to get the current weather in Bangalore. I will call the tool in the next step."}
PLAN: {"step": "TOOL", "tool": "get_weather", "input": "Bangalore"}
PLAN: {"step": "OBSERVE", "tool": "get_weather", "output": "Weather in Bangalore: 25°C, Partly cloudy"}
PLAN: {"step": "PLAN", "content": "I got the result from tool get_weather which is 'Weather in Bangalore: 25°C, Partly cloudy'. I will use this information to provide the final answer to the user."}
OUTPUT: {"step": "OUTPUT", "content": "The current weather in Bangalore is 25°C, Partly cloudy."}

 """

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

class OutputParser(BaseModel):
    step: str = Field(..., description="The step can be START or PLAN or TOOL or OUTPUT")
    content: Optional[str] = Field(None, description="The content of the step")
    tool: Optional[str] = Field(None, description="The tool to be used in case step is TOOL")
    input: Optional[str] = Field(None, description="The input to be provided to the tool in case step is TOOL")
    output: Optional[str] = Field(None, description="The output returned by the tool in case step is OBSERVE")

while True:

    print("\n\n\n")
    user_query = input("User: ")
    message_history.append({"role": "user", "content": user_query})

    while True:
        response = client.chat.completions.parse(
            model='gpt-4o-mini',
            response_format=OutputParser,
            messages= message_history
        )

        raw_result = response.choices[0].message.content
        message_history.append({"role": "assistant", "content":raw_result})
        parsed_result = response.choices[0].message.parsed

        if parsed_result.step =="START":
            print(f"START: {parsed_result.content}")
            continue

        if parsed_result.step=="PLAN":
            print(f"PLAN: {parsed_result.content}")
            continue

        if parsed_result.step=="TOOL":
            tool_to_call = parsed_result.tool
            tool_input = parsed_result.input

            if tool_to_call in available_tools:
                tool_response = available_tools[tool_to_call](tool_input)
                print(f"TOOL: {tool_to_call} with input {tool_input}    returned output {tool_response}")
                message_history.append({"role": "assistant", "content":     json.dumps({
                    "step": "OBSERVE",
                    "tool": tool_to_call,
                    "output": tool_response
                })})                  
            continue

        if parsed_result.step=="OUTPUT":
            print(f"OUTPUT: {parsed_result.content}")
            break

print("\n\n\n")