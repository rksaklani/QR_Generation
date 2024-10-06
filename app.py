from flask import Flask, render_template, request, jsonify
import pyqrcode as qr
from io import BytesIO
from PIL import Image as Img
import base64
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_qr():
    link = request.form.get('url')
    
    # Create the QR code
    QR_Code = qr.create(link)
    
    # Save the QR code to an in-memory file
    buffer = BytesIO()
    QR_Code.png(buffer, scale=5)
    buffer.seek(0)
    
    # Convert the buffer to an image
    img = Img.open(buffer)
    
    # Encode the image as base64
    img_buffer = BytesIO()
    img.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    img_data = base64.b64encode(img_buffer.read()).decode('utf-8')

    return jsonify({'qr_code': f"data:image/png;base64,{img_data}"})

if __name__ == '__main__':
    app.run(debug=True)
