from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
sys.path.append("..")
from core.model import LivingModel, ModelConfig

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

model = LivingModel()

class GenerateRequest(BaseModel):
    prompt: str

@app.on_event("startup")
async def startup():
    model.load()

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

@app.post("/generate")
def generate(request: GenerateRequest):
    output = model.generate(request.prompt)
    return {
        "prompt": request.prompt,
        "output": output,
        "model": model.config.model_name,
        "version": model.config.version
    }

@app.get("/lineage")
def lineage():
    return {
        "version": model.config.version,
        "lineage": model.config.lineage
    }

@app.get("/memory")
def get_memory():
    return {
        "stats": model.memory.stats(),
        "context": model.memory.get_context(last_n=20)
    }

@app.delete("/memory")
def clear_memory():
    model.memory.clear()
    return {"status": "memory cleared"}