import os
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter

# Flask app configuration
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
ALLOWED_EXTENSIONS = {'docx'}

def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_and_protect(docx_path, output_pdf_path, password=None):
    """
    Convert .docx to .pdf and optionally add a password to the PDF.

    Args:
        docx_path (str): Path to the input .docx file.
        output_pdf_path (str): Path to save the converted .pdf file.
        password (str, optional): Password to encrypt the PDF.
    """
    try:
        # Read the .docx file
        doc = Document(docx_path)

        # Create a PDF from the document content
        pdf = canvas.Canvas(output_pdf_path, pagesize=letter)
        width, height = letter
        y_position = height - 50  # Start from the top of the page
        line_height = 14  # Line height for text

        for para in doc.paragraphs:
            pdf.drawString(50, y_position, para.text)
            y_position -= line_height
            if y_position < 50:  # Avoid writing beyond the page
                pdf.showPage()
                y_position = height - 50
        pdf.save()

        # Add password protection if a password is provided
        if password:
            reader = PdfReader(output_pdf_path)
            writer = PdfWriter()

            for page in reader.pages:
                writer.add_page(page)

            # Encrypt the PDF with the password
            writer.encrypt(password)

            # Save the password-protected PDF
            with open(output_pdf_path, "wb") as f:
                writer.write(f)

    except Exception as e:
        # Raise a ValueError for better error messages
        raise ValueError(f"Failed to convert and protect PDF: {e}")

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Endpoint to handle file uploads and conversion.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    password = request.form.get('password')  # Get the password if provided

    # Validate uploaded file
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.pdf')

        file.save(file_path)  # Save the uploaded file

        try:
            # Convert to PDF and optionally add a password
            convert_and_protect(file_path, pdf_path, password=password)
            return send_file(pdf_path, as_attachment=True)  # Serve the PDF file for download
        except ValueError as e:
            print(f"Conversion Error: {e}")
            return jsonify({'error': f"File conversion failed: {e}"}), 500
    else:
        return jsonify({'error': 'Invalid file type. Only .docx files are allowed.'}), 400

@app.route('/')
def home():
    """
    Serve the home page with the file upload form.
    """
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)