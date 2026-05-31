import io
from colorthief import ColorThief
from PIL import Image, UnidentifiedImageError
from flask import Flask, request, jsonify

app = Flask(__name__)

SUPPORTED_FORMATS = {'PNG', 'JPEG', 'BMP', 'GIF', 'WEBP', 'TIFF'}


# Helper Functions
def rgb_to_hex(rgb):
    """Convert (r, g, b) tuple in [0, 255] to HEX string (#RRGGBB)"""
    return "#{:02X}{:02X}{:02X}".format(rgb[0], rgb[1], rgb[2])


def extract_dominant_colors(image_bytes, count):
    """
    Given raw image bytes and a count, return a list of exactly `count` dominant
    color hex strings using ColorThief's median-cut algorithm.
    """
    buf = io.BytesIO(image_bytes)
    ct = ColorThief(buf)
    palette = ct.get_palette(color_count=count, quality=5)
    return [rgb_to_hex(c) for c in palette[:count]]

# Route
@app.route('/extract', methods=['POST'])
def extract():
    # Validate file presence
    if 'image' not in request.files:
        return jsonify({"error": "image file is required (multipart/form-data field: image)"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "image file is required (multipart/form-data field: image)"}), 400

    # Validate count
    count_raw = request.form.get('count', None)
    count = 5  # default
    if count_raw is not None:
        try:
            count = int(count_raw)
        except ValueError:
            return jsonify({"error": "count must be an integer"}), 400
        if count < 3 or count > 8:
            return jsonify({"error": "count must be between 3 and 8"}), 400

    # Read and validate image format
    image_bytes = file.read()
    try:
        img = Image.open(io.BytesIO(image_bytes))
        img.verify()
        if img.format not in SUPPORTED_FORMATS:
            return jsonify({"error": "unsupported image format: {}; supported formats are {}".format(
                img.format, ', '.join(sorted(SUPPORTED_FORMATS)))}), 400
    except UnidentifiedImageError:
        return jsonify({"error": "invalid image file: could not identify image format"}), 400
    except Exception:
        return jsonify({"error": "invalid image file: could not identify image format"}), 400

    # Extract dominant colors
    colors = extract_dominant_colors(image_bytes, count)
    return jsonify({"colors": colors})


# Entry point
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)