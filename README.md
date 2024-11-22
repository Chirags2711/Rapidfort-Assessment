# Flask Application for File Upload and Conversion

This documentation provides a detailed explanation of a Flask-based application for uploading `.docx` files, converting them to PDF format, and optionally applying password protection to the generated PDF. The project also includes Docker support.

## Features
1. Upload `.docx` files through a web interface.
2. Convert uploaded files to PDF format.
3. Optionally apply password protection to the PDF.
4. Serve the converted PDF for download.
5. Includes Docker support for easy deployment.

---

## Project Structure

```
project-directory/
├── app.py                  # Main application script
├── templates/
│   └── index.html         # HTML template for the web interface
├── uploads/               # Directory for storing uploaded files
├── Dockerfile             # Docker configuration file
├── requirements.txt       # Python dependencies
```

---

## Dependencies

The project requires the following Python packages:

- **Flask**: For creating the web application.
- **Werkzeug**: For secure filename handling.
- **python-docx**: For reading `.docx` files.
- **reportlab**: For generating PDF files.
- **PyPDF2**: For adding password protection to PDFs.

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

## Flask Application Overview

### Configuration

The application uses a dedicated folder (`uploads/`) to store uploaded files. It supports only `.docx` file uploads, as defined by:

```python
ALLOWED_EXTENSIONS = {'docx'}
```

### Core Functions

#### `allowed_file(filename)`

- Verifies if the uploaded file has an allowed extension.
- Returns `True` if the file is valid, `False` otherwise.

#### `convert_and_protect(docx_path, output_pdf_path, password=None)`

- Converts a `.docx` file to a PDF.
- Adds password protection if a password is provided.
- Handles errors gracefully and raises exceptions for invalid operations.

#### `upload_file()` (Route: `/upload`)

- Handles file uploads.
- Converts the uploaded file to a PDF.
- Returns the generated PDF as a downloadable file.
- Responds with error messages for invalid files or conversion failures.

#### `home()` (Route: `/`)

- Serves the homepage with a file upload form.

### Running the Application

Run the application locally with:

```bash
python app.py
```

Access the app in your browser at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Docker Deployment

### Dockerfile

A `Dockerfile` is provided for containerizing the application. It includes the necessary configurations to run the Flask app.

```dockerfile
# Use Python 3.12 slim as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 (or any other available port)
EXPOSE 8000

# Set the environment variable to use Python 3.12
ENV FLASK_ENV=development

# Run the application, making it listen on all available network interfaces
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
```

### Building and Running the Docker Image

1. Build the Docker image:

   ```bash
   docker build -t flask-docx-to-pdf .
   ```

2. Run the container:

   ```bash
   docker run -d -p 8000:8000 flask-docx-to-pdf
   ```

Access the app at: [http://localhost:8000](http://localhost:8000)

---

## Usage Instructions

1. Open the application in a web browser.
2. Upload a `.docx` file using the form on the homepage.
3. Optionally, provide a password for the PDF.
4. Submit the form to convert the file.
5. Converted PDF will be downloaded automatically.

---

## Error Handling

- **File Conversion Error**:
  - Returns an error with a message: `"Failed to convert and/or protect PDF`

---

## Future Enhancements

1. Support for additional file formats.
2. Advanced PDF layout options.
3. Implement user authentication for secure file handling.

---

This documentation serves as a comprehensive guide for understanding, running, and deploying the Flask application. For further assistance, feel free to reach out!