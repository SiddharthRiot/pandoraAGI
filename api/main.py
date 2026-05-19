from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="PandoraAGI",
    description="Open infrastructure for building AGI democratically.",
    version="0.0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "project": "PandoraAGI",
        "status": "alive",
        "version": "0.0.1",
        "message": "AGI should belong to humanity."
    }

@app.get("/health")
def health():
    return {"status": "ok"}