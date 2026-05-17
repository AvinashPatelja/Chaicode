from google import genai

client = genai.Client(
    api_key="AIzaSyBSlPlMkGKOGZ-aNQgxdWNyC0KlNNv__Jo"
)

response  = client.models.generate_content(
  model="gemini-2.5-flash", contents="Hey, What is an MCP(Model Context Protocol)?"
)

print(response.text)