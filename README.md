# Image Color Extractor — Microservice

## 1. What this microservice does

Given an image file, the microservice returns its dominant colors as a list of HEX codes, extracted using the median-cut color quantization algorithm (via [colorthief](https://github.com/fengsp/color-thief-py)).

By default it returns 5 dominant colors. An optional `count` parameter controls how many colors are returned (3–8).

## 2. How to REQUEST data from the microservice

**The microservice must be running before any request is made.**

```bash
# Start the microservice
pip install flask pillow colorthief
python app.py
```

Send an **HTTP POST** request to:

```
http://localhost:5002/extract
```

with a **multipart/form-data** body containing:

- `image` (file, required): the image file to extract colors from; supported formats are PNG, JPEG, BMP, GIF, WEBP, TIFF
- `count` (integer, optional): number of dominant colors to return, between 3 and 8; defaults to 5

### Example requests

```python
import requests

# Default extraction — returns 5 dominant colors
with open("photo.png", "rb") as f:
    response = requests.post(
        "http://localhost:5002/extract",
        files={"image": f}
    )

# Specify count — returns 3 dominant colors
with open("photo.png", "rb") as f:
    response = requests.post(
        "http://localhost:5002/extract",
        files={"image": f},
        data={"count": 3}
    )

# Maximum count — returns 8 dominant colors
with open("photo.png", "rb") as f:
    response = requests.post(
        "http://localhost:5002/extract",
        files={"image": ("photo.png", f, "image/png")},
        data={"count": 8}
    )
```

## 3. How to RECEIVE data from the microservice

The microservice always responds with **JSON**.

### Success response — HTTP 200

```json
{
  "colors": ["#2CB464", "#8C44AC", "#FC5434", "#2C84C4", "#FCC404"]
}
```

### Error response — HTTP 400

```json
{
  "error": "invalid image file: could not identify image format"
}
```

### Example: receiving and using the data

```python
import requests

with open("photo.png", "rb") as f:
    response = requests.post(
        "http://localhost:5002/extract",
        files={"image": f},
        data={"count": 5}
    )

if response.status_code == 200:
    data = response.json()
    colors = data["colors"]    # list of HEX strings, e.g. 5 items
    print(colors)
    # → ['#2CB464', '#8C44AC', '#FC5434', '#2C84C4', '#FCC404']
else:
    error = response.json()["error"]
    print(f"Error: {error}")
```