from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="NLP Assistant", version="1.0")

class QueryRequest(BaseModel):
    question: str
    context: str = ""   # опциональный контекст

@app.post("/ask")
async def ask_question(req: QueryRequest):
    # Заглушка LLM-ответа. В production здесь будет вызов GPT-подобной модели.
    if "document" in req.question.lower():
        answer = "According to the records, the document status is 'accepted'."
    elif "amount" in req.question.lower():
        answer = "The transaction amount is within allowed limits."
    else:
        answer = "I am sorry, I cannot answer that question at the moment."
    return {"question": req.question, "answer": answer}

@app.get("/health")
async def health():
    return {"status": "ok"}
