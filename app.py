from flask import Flask, request, render_template, send_file
from PIL import Image, ImageOps
import os
from io import BytesIO

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def dummy_style_transfer(image):
    # Dummy style transfer: convert image to grayscale and then invert colors
    gray_image = ImageOps.grayscale(image)
    styled_image = ImageOps.invert(gray_image)
    return styled_image

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return "No image uploaded", 400
        file = request.files['image']
        if file.filename == '':
            return "No selected file", 400
        image = Image.open(file.stream)
        output_image = dummy_style_transfer(image)
        
        # Save to a BytesIO stream to send without saving to disk
        img_io = BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='styled.png')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
