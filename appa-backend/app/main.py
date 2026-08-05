from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="APPA Backend",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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