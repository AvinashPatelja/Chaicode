from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field
import os
import json
import requests 

load_dotenv(dotenv_path=Path(__file__).with_name('.env'))
client = OpenAI()

def run_command(cmd: str):
    result = os.system(cmd)
    return result

def get_weather(city : str):
    url = f"https://wttr.in/{city}?format=3"
    response = requests.get(url)
    if response.status_code == 200:
        return f"Weather in {response.text.strip()}"
    else:
        return f"Could not retrieve weather data for {city}."
       

available_tools = {
    "run_command": run_command,
    "get_weather": get_weather,
}

class OutputParser(BaseModel):
    step: str = Field(..., description="The step can be START or PLAN or TOOL or OUTPUT")   
    content: Optional[str] = Field(None, description="The content of the step")
    tool: Optional[str] = Field(None, description="The tool to be used in case step is TOOL")
    input: Optional[str] = Field(None, description="The input to be provided to the tool in case step is TOOL")


SYSTEM_PROMPT = """
You are an helpful assitant that answers the user queries. You will be provided with a list of tools that you can use to answer user quesries. If you find any tool is useful in answering the user query, you can call the tool and provide the input to the toll. You will get the output from the tool which you can use to answer the user query. Always try to use the tools whenever you find them useful in answering the user query.

 OUTPUT Format:
 {{
    "step": "START or PLAN or TOOL or OUTPUT",
    "content": "string"
 }}

Rules:
- Strictly follow the given JSON output format.
- Only run 1 step at a time.
- The sequence of steps should be START (Where user can give input) -> PLAN (That can be multiple steps) 
-> TOOL (Where you can use the tools to get the output that can be useful in answering the user query)
-> OUTPUT (Which is going to display the final answer to the user). Always follow this sequence.

Available tools:
- run_command(cmd: str) : Takes a command as input and executes it in the terminal.
- get_weather(city: str) : Takes city as input and provide weather details.

Example 1:
"step": "START","content": "User: List all the files and folders in current directory."
"step": "PLAN", "content": "User want to see the list of all the files and folders in the directory."
"step": "PLAN", "content": "I can use the tool run_command to execute the command."
"step": "TOOL", "tool": "run_command", "input": "ls -la"
"step": "OBSERVE", "tool": "run_command", "output": "there are 3 files and 2 folders in the current directory. And the names of files are file1.txt, file2.txt and file3.txt and the names of folders are folder1 and folder2."
"step": "OUTPUT", "content": "There are 3 files and 2 folders in the current directory. And the names of files are file1.txt, file2.txt and file3.txt and the names of folders are folder1 and folder2."

Example 2:
"step": "START", "content": "User: What is the current weather in Bangalore?"
"step": "PLAN", "content": "User wants to know the current weather in Bangalore."
"step": "PLAN", "content": "I can use the tool get_weather to get the current weather in Bangalore. I will call the tool in the next step."
"step": "TOOL", "tool": "get_weather", "input": "Bangalore"
"step": "OBSERVE", "tool": "get_weather", "output": "Weather in Bangalore: 25°C, Partly cloudy"
"step": "PLAN", "content": "I got the result from tool get_weather which is 'Weather in Bangalore: 25°C, Partly cloudy'. I will use this information to provide the final answer to the user."
"step": "OUTPUT", "content": "The current weather in Bangalore is 25°C, Partly cloudy."

"""

message_history = [
    {"role":"system", "content": SYSTEM_PROMPT}
]

while True:

    print("\n\n\n")
    user_query = input("User: ")
    message_history.append({"role": "user", "content": user_query})

    while True:
        response = client.chat.completions.parse(
            model='gpt-4o-mini',
            response_format=OutputParser,
            messages=message_history
        )

        message_history.append({"role": "assistant", "content": json.dumps(response.choices[0].message.content)})
        parsed_result = response.choices[0].message.parsed

        if parsed_result.step == "START":
            print(f"START: {parsed_result.content}")
            continue

        if parsed_result.step == "PLAN":
            print(f"PLAN: {parsed_result.content}")
            continue

        if parsed_result.step == "TOOL":
            tool_to_call = parsed_result.tool
            tool_input = parsed_result.input

            if tool_to_call in available_tools:
                tool_response= available_tools[tool_to_call](tool_input)
                message_history.append({"role": "assistant", "content": json.dumps({"step": "OBSERVE", "tool": tool_to_call, "output": tool_response})})

                print(f"TOOL: {tool_to_call} called with input: {tool_input} and got output: {tool_response}")
                continue

        if parsed_result.step == "OUTPUT":
            print(f"OUTPUT: {parsed_result.content}")
            break

