from dotenv import load_dotenv
from pathlib import Path
from openai import OpenAI
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings

load_dotenv(Path(__file__).parent / '.env')  # Load environment variables from .env file

client = OpenAI()

# Vector Embeddings
embeding_model = OpenAIEmbeddings(model="text-embedding-3-small")

# Vector DB connection
vector_db = QdrantVectorStore.from_existing_collection(
    collection_name="dotnet-interview-questions",
    embedding=embeding_model,
    url="http://localhost:6333",
)

# Take user query as input
user_query = input("Enter your query: ")

# Relevant search(chuncks) in vector DB
search_result = vector_db.similarity_search(query=user_query, k=5)

context ="\n\n\n".join([f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}" for result in search_result])

# context = "\n\n".join(
#     result.page_content
#     for result in search_result
# )

# for result in search_result:
#     print(
#         f"Page Content: {result.page_content}\n"
#         f"Page Number: {result.metadata['page_label']}\n"
#         f"File Location: {result.metadata['source']}"
#     )

# print("========== RETRIEVED CONTEXT ==========")
# print(context)

SYSTEM_PROMPT =f"""
You are an expert assistant in resolving user queries using existing context retrieved from pdf files along with page_content, page_number.
You should only answer the question based on the given context. 

Context: {context}
"""

response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT}, 
        {"role": "user", "content": user_query},
    ]
)
print("========== RETRIEVED RESULT ==========")
print(response.choices[0].message.content)