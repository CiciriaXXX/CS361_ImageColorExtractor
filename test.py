import requests
import io
import time
from PIL import Image, ImageDraw

BASE_URL = "http://localhost:5002/extract"


def call(description, files=None, data=None, expect_status=200):
    print(f"Testing {description} ...")

    start = time.time()
    with open(files, "rb") as f:
        r = requests.post(BASE_URL,files={"image": f},data=data)
    elapsed = time.time() - start

    status = "PASS" if r.status_code == expect_status else "FAIL"
    print(f"{status} HTTP {r.status_code} ({elapsed:.2f}s)")

    result = r.json()
    if "colors" in result:
        print(f"colors ({len(result['colors'])}): {result['colors']}")
    else:
        print(f"error: {result.get('error', result)}")
    print()


print("=== Image Color Extractor Test Program ===\n")

# --- User Story 1 ---
call(
    "Default extraction 1 — no count param, expect 5 colors",
    files= "test1.png"
)
call(
    "Default extraction 2 — no count param, expect 5 colors",
    files= "test2.png"
)


call(
    "Error — invalid file format",
    files="README.md",
    expect_status=400
)


# --- User Story 2: Extraction Count Control ---

call(
    "Count = 3 (minimum)",
    files="test1.png",
    data={"count": 3}
)

call(
    "Count = 8 (maximum)",
    files="test2.png",
    data={"count": 8}
)

call(
    "Count = 5 (explicit)",
    files = "test1.png",
    data={"count": 5}
)

call(
    "Error — count = 2 (below minimum)",
    files = "test1.png",
    data={"count": 2},
    expect_status=400
)

call(
    "Error — count = 9 (above maximum)",
    files = "test1.png",
    data={"count": 9},
    expect_status=400
)

call(
    "Error — count is not an integer",
    files = "test1.png",
    data={"count": "many"},
    expect_status=400
)

print("=== Done ===")
