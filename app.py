from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import re

from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_ui():
    return FileResponse("static/index.html")


def extract_entities(code: str, filename: str):
    entities = []
    lines = code.split("\n")
    for i, line in enumerate(lines, 1):
        func_match = re.match(r'^\s*def\s+(\w+)\s*\(', line)
        if func_match:
            entities.append({"name": func_match.group(1), "type": "function", "file": filename, "line": i})
        class_match = re.match(r'^\s*class\s+(\w+)', line)
        if class_match:
            entities.append({"name": class_match.group(1), "type": "class", "file": filename, "line": i})
        js_func = re.match(r'^\s*(async\s+)?function\s+(\w+)\s*\(', line)
        if js_func:
            entities.append({"name": js_func.group(2), "type": "function", "file": filename, "line": i})
    return entities


def build_chain():
    llm = Ollama(model="codellama", temperature=0)

    prompt = PromptTemplate.from_template("""
You are a code analysis assistant. Use the code below to answer the question.
Give a clear answer. If asked about a function, explain what it does in 1-2 sentences.

Code context:
{context}

Question: {question}

Answer:""")

    chain = prompt | llm | StrOutputParser()
    return chain


@app.post("/summarize")
async def summarize(file: UploadFile = File(...), project_name: str = Form("")):
    content = await file.read()
    code = content.decode("utf-8", errors="replace")
    filename = file.filename

    entities = extract_entities(code, filename)
    try:
        chain = build_chain()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    results = []
    for entity in entities:
        question = f"What does the {entity['type']} '{entity['name']}' do? One or two sentences only."
        try:
            description = chain.invoke({"context": code, "question": question}).strip()
        except Exception as e:
            description = "Could not generate description."

        results.append({
            "name": entity["name"],
            "type": entity["type"],
            "file": entity["file"],
            "line": entity["line"],
            "description": description
        })

    return {
        "project": project_name or filename,
        "filename": filename,
        "entity_count": len(results),
        "entities": results
    }


class QuestionRequest(BaseModel):
    code: str
    question: str

@app.post("/ask")
async def ask(req: QuestionRequest):
    chain = build_chain()
    answer = chain.invoke({"context": req.code, "question": req.question}).strip()
    return {"answer": answer}