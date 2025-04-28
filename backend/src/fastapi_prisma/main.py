from datetime import datetime

from fastapi import FastAPI, Response
from pydantic import BaseModel

from prisma import Prisma
from prisma import errors as prisma_errors

prisma = Prisma()


async def lifespan(app: FastAPI):
    await prisma.connect()
    yield
    await prisma.disconnect()


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok"}


class PlaceModel(BaseModel):
    id: int
    place: str
    latitude: float
    longitude: float
    pic_file: str


@app.get("/places")
async def get_places(page: int = 1) -> list[PlaceModel]:
    per_page = 1000
    try:
        return await prisma.place.find_many(take=per_page, skip=(page - 1) * per_page)
    except prisma_errors.PrismaError as e:
        print(e)
        return Response(status_code=400, content="fetch failed")


class PlacePost(BaseModel):
    place: str
    latitude: float
    longitude: float
    pic_file: str


@app.post("/places", status_code=201)
async def create_place(data: PlacePost) -> PlaceModel:
    try:
        return await prisma.place.create({"place": data.place,"latitude":data.latitude,"longitude":data.longitude,"pic_file": data.pic_file})
    except prisma_errors.PrismaError as e:
        print(e)
        return Response(status_code=400, content="create failed")


@app.delete("/places/{place_id}")
async def delete_place(place_id: int):
    try:
        await prisma.place.delete(where={"id": place_id})
        return Response(status_code=204)
    except prisma_errors.PrismaError as e:
        print(e)
        return Response(status_code=400, content="delete failed")


class PlacePatch(BaseModel):
    place: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    pic_file: str | None = None


@app.patch("/places/{place_id}")
async def update_place(place_id: int, place: PlacePatch) -> PlaceModel:
    try:
        return await prisma.place.update(
            where={"id": place_id}, data=place.model_dump(exclude_unset=True)
        )
    except prisma_errors.PrismaError as e:
        print(e)
        return Response(status_code=400, content="update failed")