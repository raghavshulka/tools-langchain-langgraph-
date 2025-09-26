import array
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel, field_validator

app = FastAPI()

class todoType(BaseModel):
    topic: str
    todo: str
    status: str


    @field_validator('topic')
    @classmethod
    def uppercaseTopic(cls,value):
        return value.upper()


arr = []

@app.get("/")
def root():
    return {"hello from server"}


@app.get("/todos", response_model=List[todoType])
def get_todos():
    return arr


@app.post("/set")
def set_todos(data:todoType):
    arr.append(data)
    return data 



@app.delete("/delete/{title}")
def delete_todo(title: str):
    for i, todo in enumerate(arr):
        if todo.topic == title:
            print(todo,title)
            removed = arr.pop(i)
            return {"message": f"Deleted todo '{removed}'"}
    


