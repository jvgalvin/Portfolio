import logging
import os

from fastapi import FastAPI, Request, Response
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis

from pydantic import BaseModel, validator
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

model_path = "./distilbert-base-uncased-finetuned-sst2"
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
classifier = pipeline(
    task="text-classification",
    model=model,
    tokenizer=tokenizer,
    device=-1,
    top_k=None,
)

logger = logging.getLogger(__name__)
LOCAL_REDIS_URL = "redis://redis:6379"
app = FastAPI()

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://redis:6379")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

class SentimentRequest(BaseModel):
    text: list[str]

    @validator("text")
    def not_empty(cls, v):
        if len(v) < 1:
            raise ValueError("Must pass something - cannot pass empty list")
        return v

class Sentiment(BaseModel):
    label: str
    score: float

class SentimentResponse(BaseModel):
    predictions: list[list[Sentiment]]

@app.post("/predict", response_model=SentimentResponse)
@cache(expire=100)
async def predict(sentiments: SentimentRequest):
    return {"predictions": classifier(sentiments.text)}

@app.get("/health")
async def health():
    return {"status": "healthy"}