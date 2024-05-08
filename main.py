from fastapi import FastAPI

app = FastAPI()

@app.post("/students/")
async def create_student(student: int):
    return "Hello"

@app.get("/students/{student_id}")
async def get_student(student_id: int):
    return student_id

@app.get("/")
async def root():
    return {"message": "Hello World"}