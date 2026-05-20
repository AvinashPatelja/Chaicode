from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field
import os
import json

load_dotenv(dotenv_path=Path(__file__).with_name('.env'))
client = OpenAI()

def run_command(cmd: str):
    result = os.system(cmd)
    return result

available_tools = {
    "run_command": run_command
}

class OutputParser(BaseModel):
    step: str = Field(..., description="The step can be START or PLAN or TOOL or OUTPUT")   
    content: Optional[str] = Field(None, description="The content of the step")
    tool: Optional[str] = Field(None, description="The tool to be used in case step is TOOL")
    input: Optional[str] = Field(None, description="The input to be provided to the tool in case step is TOOL")

SYSTEM_PROMPT = """
You are an helpful assitant that answers the user queries. You will be provided with a list of tools that you can use to answer user quesries. If you find any tool is usful in answering the user quesry, you can call the tool and provide the input to the toll. You will get the output from the tool which you can use to answer the user query. Always try to use the tools whenever you find them useful in answering the user query.

Rules:
- Strictly follow the given JSON output format.
- Only run 1 step at a time.
- The sequence of steps should be START (Where user can give input) -> PLAN (That can be multiple steps) 
-> TOOL (Where you can use the tools to get the output that can be useful in answering the user query)
-> OUTPUT (Which is going to display the final answer to the user). Always follow this sequence.

Available tools:
- run_command(cmd: str) : Takes a command as input and executes it in the terminal.

Example 1:
"step": "START","content": "User: List all the files and folders in current directory."
"step": "PLAN", "content": "User want to see the list of all the files and folders in the directory."
"step": "PLAN", "content": "I can use the tool run_command to execute the command."
"step": "TOOL", "tool": "run_command", "input": "ls -la"
"step": "OBSERVE", "tool": "run_command", "output": "there are 3 files and 2 folders in the current directory. And the names of files are file1.txt, file2.txt and file3.txt and the names of folders are folder1 and folder2."
"step": "OUTPUT", "content": "There are 3 files and 2 folders in the current directory. And the names of files are file1.txt, file2.txt and file3.txt and the names of folders are folder1 and folder2."

"""

mesage_history = [
    {"role":"system", "content": SYSTEM_PROMPT}
]

user_query = input("User: ")
mesage_history.append({"role": "user", "content": user_query})

respo