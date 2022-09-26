import sys
sys.path.append('../../libs/kafka_lib')
sys.path.append('../../libs/mongodb_lib')
sys.path.append('../../utils/protobuf/py/')

import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException

# from src.kafka.producer import FramesKafkaProducer
from src.routes import media

app = FastAPI()

app.include_router(media.router)

@app.get("/")
async def root():
    raise HTTPException(status_code=404, detail="Endpoint not found")