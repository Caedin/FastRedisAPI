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
    print(f"Request received for GET {key}/json")
    dbval = redis_helper.get_json(key, path)
    if dbval == "":
        print("No value found in db")
        return ""
    print("success")
    return dbval

@app.post("/{key}/json")
async def post_json(key, request: Request, path: Optional[str] = "."):
    print(f"Request received for SET {key}/json")
    val = await request.json()
    redis_helper.set_json(key, path, val)
    print("success")

@app.delete("/{key}/json")
async def delete_json(key):
    print(f"Request received for DELETE {key}/json")
    redis_helper.delete(key)
    print("success")

@app.get("/{key}/pop")
async def pop(key, path: Optional[str] = ".", index: Optional[int] = -1):
    print(f"Request received for POP {key}/json")
    redis_helper.pop_json_array(key, path, index)
    print("success")

@app.post("/{key}/insert")
async def insert(key, request: Request, path: Optional[str] = ".", index: Optional[int] = 0):
    print(f"Request received for INSERT {key}/json")
    val = await request.body()
    redis_helper.insert_json_array(key, path, index, val.decode("utf8"))
    print("success")

@app.get("/{key}", response_model=str)
async def get(key: str):
    print(f"Request received for GET {key}")
    dbval = redis_helper.get(key)
    if dbval == "":
        print("No value found in db")
        return ""
    print("success")
    return dbval

@app.post("/{key}")
async def post(key, request: Request, ttl: Optional[int] = 0):
    val = await request.body()
    print(f"Request received for SET {key} with value {str(val)}")
    redis_helper.set(key, str(val), ttl)
    print("success")

@app.delete("/{key}")
async def delete(key):
    print(f"Request received for DELETE {key}")
    redis_helper.delete(key)
    print("success")

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("API_PORT")),
        reload=True,
        ssl_keyfile="./server.key",
        ssl_certfile="./server.crt"
    )