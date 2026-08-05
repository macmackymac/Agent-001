from fastapi import FastAPI

app = FastAPI(
    title="APPA Backend",
    version="0.1.0"
)


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