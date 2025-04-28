To add data:
- prepare geojson file with the following attributes:
  - place: str
  - latitude: float
  - longitude: float
  - pic_file: str

- target geojson file in geojson_importer.py

run

```
uv run python geojson_importer.py
uv run prisma migrate dev
```