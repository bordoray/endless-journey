from fastapi import FastAPI, Query

from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic import BaseModel
from starlette.responses import Response
from geojson_pydantic import FeatureCollection

import httpx
import random

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


## 1 current time
@app.get("/current_time")
def current_time():

    time_tokyo = datetime.now(ZoneInfo("Asia/Tokyo"))
    time_paris = datetime.now(ZoneInfo("Europe/Paris"))

    return {
        "tokyo": f"{time_tokyo:%Y-%m-%d %H:%M:%S}",
        "paris": f"{time_paris:%Y-%m-%d %H:%M:%S}",
    }

## 2 Fibonacci

class FibonacciResponse(BaseModel):
    result: int


def fibonacci(n: int) -> int:
    a, b = 0, 1
    if n == 0:
        return a
    if n == 1:
        return b
    for i in range(n - 1):
        a, b = b, a + b
    return b


@app.get("/fibonacci")
def get_nb_fibonacci(n: int = Query(ge=1, le=1024)) -> FibonacciResponse:
    return FibonacciResponse(result=fibonacci(n))

## 3 randon tiles

tile_urls = [
    r"https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png",
    r"https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png",
    r"https://tile.openstreetmap.org/{z}/{x}/{y}.png",
]


@app.get("/tiles/{x}/{y}/{z}/")
async def get_tiles(
    z: int,
    x: int,
    y: int,
):
    url = (
        random.choice(tile_urls)
        .replace("{z}", str(z))
        .replace("{x}", str(x))
        .replace("{y}", str(y))
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 200:
        return Response(
            content=response.content,
            media_type=response.headers.get("content-type", "image/png"),
        )
    else:
        #show error
        print (response.content)
        return Response(
            content=response.content,
            status_code=response.status_code,
            media_type=response.headers.get("content-type", "text/plain"),
        )


## Stats of geojson
@app.post("/geojson_stats/")
async def geojson_stats(item: FeatureCollection):
    features_count = len(item.features)
    if item.features and item.features[0].properties:
        properties_count = len(item.features[0].properties)
    else:
        properties_count = 0

    # Response
    return { "features_count": features_count, "attributes_count": properties_count }

