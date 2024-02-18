from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import io
import zipfile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    pdf_file = request.files['pdfInput']

    if not pdf_file or not pdf_file.filename.endswith('.pdf'):
        return 'Invalid PDF file', 400

    pdf_reader = PdfReader(io.BytesIO(pdf_file.read()))
    num_pages = len(pdf_reader.pages)

    image_list = convert_from_path(pdf_file.filename, 500, first_page=1, last_page=num_pages)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zip_file:
        for i, image in enumerate(image_list):
            image.save(f'page_{i + 1}.jpg', 'JPEG')
            zip_file.write(f'page_{i + 1}.jpg')

    zip_buffer.seek(0)
    return send_file(zip_buffer, download_name='all_pages_images.zip', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
