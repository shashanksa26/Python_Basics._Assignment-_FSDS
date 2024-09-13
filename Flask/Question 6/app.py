from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from urllib.parse import quote

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Function to render the file upload form
@app.route('/')
def upload_form():
    return render_template('upload.html')

# Function to handle file uploading
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return redirect(url_for('display_file', filename=file.filename))
    return "File upload failed"

# Function to display the uploaded file on the website
@app.route('/display/<filename>')
def display_file(filename):
    encoded_filename = quote(filename)  # Encode filename for URL
    return f'<img src="/uploads/{encoded_filename}" style="max-width:100%;">'



# Route to serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
