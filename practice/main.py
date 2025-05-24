from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price:float

app=FastAPI(
    title="My First FastAPI App",
    description="This is a simple FastAPI Application for learning purpose.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message":"Hello, FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id:int):
    return {"item_id":item_id}

@app.post("/items/")
def create_items(item:Item):
    return {"name":item.name,"price":item.price}

@app.put("/items/{item_id}")
def update_item(item_id:int,item:Item):
    return {"item_id":item_id,"name":item.name,"price":item.price}

@app.delete("/items/{item_id}")
def delete_item(item_id:int):
    return {"message":f"Item with id {item_id} has been deleted"}

# path parameters are part of the URL itself and are defined within
#  curly braces {}. 

#  Query parameters are optional parameters that are passed in the URL after a
#  question mark ?. Multiple query parameters are separated by an ampersand &. Query
#  parameters are often used for filtering, sorting, or pagination

@app.get("/items/")
def read_items(skip:int=0,limit:int=10):
    return {"skip":skip,"limit":limit}

@app.get("/items/{item_id}")
def read_items(item_id:int,detail:bool=False):
    if detail:
        return {"item_id":item_id,"detail":"Full item details"}
    return {"item_id":item_id}