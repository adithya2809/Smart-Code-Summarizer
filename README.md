# Smar Code Summarizer

A simple FastAPI-based code summarization service that uses Ollama through LangChain to analyze source code and generate short descriptions for detected functions, classes, and JavaScript functions.

## Project structure

- `app.py` - FastAPI application with endpoints for code summarization and direct question answering.
- `requirements.txt` - Python dependencies.
- `static/` - Static frontend files served at the root URL.
- `satic/` - appears to be an extra directory and is not used by the application.

## Features

- `GET /` - serves the static frontend from `static/index.html`
- `POST /summarize` - upload a code file and receive extracted entities with generated descriptions
- `POST /ask` - send arbitrary code and a question, receive an LLM-generated answer

## Requirements

- Python 3.10+ recommended
- `requirements.txt` dependencies:
  - `fastapi`
  - `uvicorn`
  - `python-multipart`
  - `langchain`
  - `langchain-community`
  - `faiss-cpu`
  - `ollama`

## Installation

1. Create and activate a virtual environment:

```powershell
cd "c:\Users\Aditya\Downloads\Smar code summarizer"
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

## Run the app

Start the FastAPI server with Uvicorn:

```powershell
uvicorn app:app --reload
```

Then open:

- `http://127.0.0.1:8000/` for the UI
- `http://127.0.0.1:8000/docs` for the OpenAPI docs

## API Usage

### Summarize code

`POST /summarize`

Form data:
- `file` - the uploaded source code file
- `project_name` - optional project name

Response:
- `project` - project name or filename
- `filename` - uploaded file name
- `entity_count` - number of detected entities
- `entities` - array of detected functions/classes with descriptions

### Ask a question

`POST /ask`

JSON body:
```json
{
  "code": "print(\"hello world\")",
  "question": "What does this code do?"
}
```

Response:
- `answer` - generated answer from the LLM

## Notes

- The app uses `Ollama` with the `codellama` model. Make sure Ollama is installed and configured on your machine.
- If you want the project to serve a frontend, keep the `static/` directory and update `static/index.html` as needed.
- The backend currently extracts Python functions, classes, and JavaScript-style functions by simple regex.

👤 Author
Adithya Vardhan

GitHub: @adithya2809
LinkedIn: [https://www.linkedin.com/in/adithya-vardhan-b040b0334/]

