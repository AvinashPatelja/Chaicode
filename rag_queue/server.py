from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).with_name('.env'))

from fastapi import FastAPI, Query
from .client.rq_client import queue
from .queue.worker import process_query

app = FastAPI()


@app.get("/")
async def root():
    return {"status": "Server is running!"}

@app.post("/chat")
async def chat(query: str = Query(..., description="User query to process")):
    job = queue.enqueue(process_query, query)

    return {"status": "Query enqueued!", "job_id": job.id}

@app.get("/job_status")
async def get_result(job_id: str):
    job = queue.fetch_job(job_id)
    result = job.return_value()

    return {"status": "Result retrieved!", "result": result}

    