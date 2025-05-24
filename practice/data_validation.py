#  In FastAPI, data validation is an essential aspect of building reliable and secure APIs.
#  FastAPI integrates Pydantic, a powerful data validation and parsing library, to handle
#  the validation of incoming data.

from pydantic import BaseModel, validator, Field
from fastapi import FastAPI, status, HTTPException
from datetime import datetime
from fastapi.responses import JSONResponse
# class Item(BaseModel):
#     name:str
#     price:float
#     description:str=None
#     tax:float=None
#     @validator('tax')
#     def validate_tax(cls,v):
#         if v is not None and v<0:
#             raise ValueError('Tax cannot be negative')
#         return v

app=FastAPI()

# @app.post("/items/")
# async def create_item(item:Item):
#     return {"name":item.name,"price":item.price}

# class Item(BaseModel):
#     name: str=Field(...,min_length=3)
#     price: float=Field(...,ge=0)
#     description:str=None
#     tax:float=Field(0.0,ge=0)

# If the validation fails (for example, if price is negative or name is shorter than 3
#  characters), FastAPI will automatically return a validation error.


# FastAPI supports parsing incoming data in various formats, with JSON being one of
#  the most commonly used formats for web APIs. When a client sends a JSON payload
#  to the server, FastAPI automatically converts this data into Python objects that can be
#  used by your endpoints. This process relies on Pydantic models, which ensure that the
#  data is validated and conforms to the specified structure.

class Item(BaseModel):
    name: str
    price: float
    description:str=None
    tax:float=None

# @app.post("/items/",status_code=status.HTTP_201_CREATED)
# async def create_item(item:Item):
#     return {"name":item.name,"price":item.price}

@app.post("/items/")
async def create_item(item:Item):
    response_data={
        "timestamp":datetime.now().isoformat(),
        "data":{"name":item.name,"price":item.price}
    }
    return JSONResponse(content=response_data)

