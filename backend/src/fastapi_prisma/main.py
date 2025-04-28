from datetime import datetime

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from prisma import Prisma
from prisma import errors as prisma_errors
from pydantic import BaseModel

prisma = Prisma()


async def lifespan(app: FastAPI):
    await prisma.connect()
    yield
    await prisma.disconnect()


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


class TodoModel(BaseModel):
    id: int
    title: str
    done: bool
    createdAt: datetime
    updatedAt: datetime


@app.get("/todos")
async def get_todos(page: int = 1) -> list[TodoModel]:
    per_page = 10
    try:
        return await prisma.todo.find_many(take=per_page, skip=(page - 1) * per_page)
    except prisma_errors.PrismaError as e:
        print(e)
        return Response(status_code=400, content="fetch failed")


class TodoPost(BaseModel):
    title: str


@app.post("/todos", status_code=201)
async def create_todo(todo: TodoPost) -> TodoModel:
    try:
        return await prisma.todo.create({"title": todo.title})
    except prisma_errors.PrismaError as e:
        print(e)
        return Response(status_code=400, content="create failed")


@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    try:
        await prisma.todo.delete(where={"id": todo_id})
        return Response(status_code=204)
    except prisma_errors.PrismaError as e:
        print(e)
        return Response(status_code=400, content="delete failed")


class TodoPatch(BaseModel):
    title: str | None = None
    done: bool | None = None


@app.patch("/todos/{todo_id}")
async def update_todo(todo_id: int, todo: TodoPatch) -> TodoModel:
    try:
        return await prisma.todo.update(
            where={"id": todo_id}, data=todo.model_dump(exclude_unset=True)
        )
    except prisma_errors.PrismaError as e:
        print(e)
        return Response(status_code=400, content="update failed")
