from fastapi import FastAPI

app = FastAPI(title="NLP Assistant", version="1.0")

@app.post("/assistant/ask")
async def ask(question: str):
    # В production здесь будет вызов LLM с поиском по документам
    answer = f"This is a stub answer for: '{question}'"
    return {"question": question, "answer": answer}

@app.get("/health")
async def health():
    return {"status": "ok"}
