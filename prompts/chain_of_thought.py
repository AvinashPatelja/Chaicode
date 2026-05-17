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

response = client.chat.completions.create(
    model='gpt-4o-mini',
    response_format={"type": "json_object"},
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT}, 
        {"role": "user", "content": "Write a code to add n numbers in c#"},

        #Manually keep adding messages to History
        {"role": "assistant", 
         "content": json.dumps({ "step": "START",  
        "content": "User wants a C# code to add n numbers."
        })},

        {"role": "assistant", 
         "content": json.dumps({"step": "PLAN", 
         "content": "I will create a C# program that prompts the user to enter a number n, and then allows them to input n numbers, which will be summed up."})
        },

        {"role": "assistant", 
         "content": json.dumps({"step": "PLAN", 
         "content": "The program will use a loop to read n numbers and accumulate their sum."})},

         {"role": "assistant", 
         "content": json.dumps({"step": "PLAN", "content": "I will write the C# code that includes necessary namespaces, defines the Main method, and implements the input and summing logic."})},

        {"role": "assistant",
        "content": json.dumps({"step": "OUTPUT", 
        "content": "Here's a simple C# code to add n numbers:\n\n```csharp\nusing System;\n\nclass Program\n{\n    static void Main(string[] args)\n    {\n        Console.WriteLine(\"Enter the number of elements to add:\");\n        int n = Convert.ToInt32(Console.ReadLine());\n        int sum = 0;\n\n        for (int i = 0; i < n; i++)\n        {\n            Console.WriteLine($\"Enter number {i + 1}:\");\n            int number = Convert.ToInt32(Console.ReadLine());\n            sum += number;\n        }\n\n        Console.WriteLine($\"The sum of the numbers is: {sum}\");\n    }\n}\n```"})}
    ]
)

print(response.choices[0].message.content)