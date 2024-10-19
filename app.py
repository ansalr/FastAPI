from fastapi import FastAPI, Path, HTTPException
from typing import Optional
from pydantic import BaseModel

class Student(BaseModel):
    name: str
    age: int
    grade: Optional[str]

class Updatestudent(BaseModel):
    name:Optional[str] = None
    age:Optional[int] = None
    grade:Optional[str] = None 


app = FastAPI()

students = {}
    

@app.get("/")
def index():
    return students

@app.get("/get-student/{id}")
# def studentId(id:int = Path(... , description="id is required",gt=0, lt=3)):
def studentId(id:int = Path(... , description="id is required")):
    if id in students.keys():
        return students[id]
    else:
        raise HTTPException(status_code=404, detail="Id not Exist")
    
@app.get("/get-by-name")
def Get_by_name(name:str, key:Optional[str]='name'):
        userDetail = next(filter(lambda x:x[key] == name, students.values()),"user not found")
        res = {"request":"sucess","data":userDetail}
        return res
@app.post("/add-student/{id}")
def add_student(id:int, student:Student):
    if id not in students.keys():
        students[id]={
            "name":student.name,
            "age": student.age,
            "grade": student.grade
        }
        return {"request":"sucess","data":students}
    else: 
        raise HTTPException(status_code=404, detail="Id already Exist")

@app.put('/update{id}')
def update_student(id:int, student:Updatestudent):
    if id in students.keys():
        for key,value in student:
            if value != None:
                students[id][key] = value
        return {"request":"sucess","data":students}
    else: 
        raise HTTPException(status_code=404, detail="Id not Exist")

@app.delete('/delete')
def delete_student(id:int):
    if id in students.keys():
        students.pop(id)
        return {"request":"sucess","data":students}
    else: 
        raise HTTPException(status_code=404, detail="Id not Exist")