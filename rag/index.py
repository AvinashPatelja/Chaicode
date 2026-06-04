from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / '.env')  # Load environment variables from .env file

# -> pip install -qU langchain-community
# -> pip install -qU langchain-text-splitter
pdf_path = Path(__file__).parent / 'DotNetInterviewQuestions.pdf'
loader = PyPDFLoader(file_path=pdf_path)

# STEP1 -> Load Documents
docs = loader.load()

# STEP2 -> Split Documents into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(docs)

# STEP3 -> Vector Embeddings
embeding_model = OpenAIEmbeddings(model="text-embedding-3-small")

# STEP4 -> Create Vector Store and Indexing
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embeding_model,
    collection_name="dotnet-interview-questions",
    url="http://localhost:6333",
)

print("Indexing completed successfully!")