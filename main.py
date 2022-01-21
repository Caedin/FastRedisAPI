from fastapi import Request, FastAPI
import redis_helper
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/{key}/json")
async def get_json(key, path: Optional[str] = "."):
    return redis_helper.get_json(key, path)

@app.post("/{key}/json")
async def post_json(key, request: Request, path: Optional[str] = "."):
    redis_helper.set_json(key, path, await request.json())

@app.delete("/{key}/json")
async def delete_json(key):
    redis_helper.delete(key)

@app.get("/{key}/pop")
async def pop(key, path: Optional[str] = ".", index: Optional[int] = -1):
    redis_helper.pop_json_array(key, path, index)

@app.post("/{key}/insert")
async def insert(key, request: Request, path: Optional[str] = ".", index: Optional[int] = 0):
    val = await request.body()
    redis_helper.insert_json_array(key, path, index, val.decode("utf8"))

@app.get("/{key}", response_model=str)
async def get(key: str):
    return redis_helper.get(key)

@app.post("/{key}")
async def post(key, request: Request, ttl: Optional[int] = 0):
    val = await request.body()
    redis_helper.set(key, val.decode("utf8"), ttl)

@app.delete("/{key}")
async def delete(key):
    redis_helper.delete(key)

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("API_PORT")),
        reload=True,
        ssl_keyfile="./server.key",
        ssl_certfile="./server.crt"
    )