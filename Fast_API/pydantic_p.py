from datetime import datetime
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str="Praveen Kumar"
    signup_ts: datetime|None=None
    friends: list[str]=[]

external_data={
    "id":"9347",
    "signup_ts":"2004-08-27 12:22",
    "friends":["Ashwin","Akhil","Sai Pavan"]
}

user = User(**external_data)

print(user)

print(user.friends)

from typing import Annotated

def say_hello(name: Annotated[str, "This is just metadata"])->str:
    return f"Hello {name}"