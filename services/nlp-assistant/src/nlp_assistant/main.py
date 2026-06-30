from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="NLP Assistant", version="1.0")

class Question(BaseModel):
    text: str

@app.post("/assistant/ask")
async def ask(question: Question):
    # В production здесь будет вызов LLM с RAG по логам и документам
    if "подозрительные" in question.text.lower():
        return {"answer": "За сегодня обнаружено 3 подозрительных документа: 123, 456, 789"}
    elif "статус" in question.text.lower():
        return {"answer": "Документы в обработке: 12. Завершены: 45. Требуют ручной проверки: 5."}
    return {"answer": "Извините, я пока не могу ответить на этот вопрос. Обратитесь к Runbook."}

@app.get("/health")
async def health():
    return {"status": "ok"}
