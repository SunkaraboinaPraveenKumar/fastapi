from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()

@app.get("/")
async def read_results():
    results=await some_library()
    return results

# Modern versions of Python have support for "asynchronous code" 
# using something called "coroutines", with async and await syntax.