from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv(dotenv_path=Path(__file__).with_name('.env'))
client = OpenAI()

embeding_model = OpenAIEmbeddings(model="text-embedding-3-large")

vector_db = QdrantVectorStore.from_existing_collection(
    collection_name="react-interview-questions",
    embedding=embeding_model,
    url="http://localhost:6333",
)

user_query = input("Enter your query: ")

search_result = vector_db.similarity_search(user_query, k=5)

context ="\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_result])


SYSTEM_PROMPT = """
You are an expert assistant in resolving user queries using existing context retrieved from pdf files along with page_content, page_number.
You should only answer the question based on the given context.

Context:{context}
"""

response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]
)

print("========== RETRIEVED RESULT ==========")
print(response.choices[0].message.content)
