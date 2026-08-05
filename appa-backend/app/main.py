from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="APPA Backend",
    version="0.1.0"
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.get("/")
def root():
    return {
        "message": "APPA Backend Running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    return ChatResponse(
        response=f"Hello! You said: {request.message}"
    )