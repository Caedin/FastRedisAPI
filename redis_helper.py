import redis
import os
import json

rdb = None

def is_json(myjson):
  try:
    t = json.loads(myjson)
    return t
  except ValueError as e:
    return None

def connect():
    global rdb
    if rdb is None:
        host = os.getenv("DB_HOST")
        port = os.getenv("DB_PORT")
        rdb = redis.Redis(host=host, port=port)
    return rdb

def go(f):
    rdb = connect()
    return f(rdb)

# Basic Redis
def get(key: str):
    return go(lambda rdb: rdb.get(key))
    
def set(key: str, val: str):
    return go(lambda rdb: rdb.set(key, val))

def delete(key: str):
    return go(lambda rdb: rdb.delete(key))


# Redis JSON
def get_json(key: str, path: str = "."):
    return go(lambda rdb: rdb.json().get(key, path))

def set_json(key: str, path: str = ".", val: dict = dict()):
    return go(lambda rdb: rdb.json().get(key, path, json.dumps(val)))

def pop_json_array(key: str, path: str = ".", index: int = -1):
    return go(lambda rdb: rdb.json().arrpop(key, path, index))

def insert_json_array(key: str, path: str = ".", index: int = 0, val: str = ""):
    print(f"INSERTING {val} at {key}.{path} with index {index}")
    return go(lambda rdb: rdb.json().arrinsert(key, path, index, is_json(val) or val))