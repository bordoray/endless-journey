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

result

<img width="607" alt="image" src="https://github.com/user-attachments/assets/e994f24a-7f9a-4f5a-ae3f-24b55b39a902" />
