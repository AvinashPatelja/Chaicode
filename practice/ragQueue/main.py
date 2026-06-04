from .server import app
import uvicorn
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).with_name('.env'))

def main():
    uvicorn.run(app, port=8000, host="0.0.0.0")

main()