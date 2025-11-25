from fastapi import FastAPI
from pydantic import BaseModel
from models.baseline_classifier import predict

app = FastAPI(title="Fake News Detector API")

class ArticleIn(BaseModel):
    title: str = ""
    text: str

@app.post("/analyze")
def analyze(article: ArticleIn):
    classification = predict(article.text)
    verification = {"verdict": "not_implemented", "confidence": None, "evidence": []}
    return {"classification": classification, "verification": verification}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)
