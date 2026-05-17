from google import genai

client = genai.Client(
    api_key="AIzaSyAoxvcNtmKpwLxsGEtmHXM20POYTxKQtPw",
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

response = client.chats.completions.create(
    model = "gemini-2.5-flash",
    messages = [
        {"role": "user", "content": "Hey, What is an MCP(Model Context Protocol)?"}
    ]
)

print(response.choices[0].message.content)
