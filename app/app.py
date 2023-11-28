import os
import random
import string
from click import wrap_text
from flask import Flask, jsonify, render_template, request, send_from_directory, url_for
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from flask_cors import CORS
import openai 


app = Flask(__name__, template_folder='my_templates')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/content')
def content():
    return render_template('content.html')

def wrap_text(text, max_width, font_name, font_size):
    # Function to wrap text
    wrapped_text = []
    words = text.split()

    while words:
        line = ''
        while words and stringWidth(line + words[0], font_name, font_size) <= max_width:
            line += (words.pop(0) + ' ')
        wrapped_text.append(line)

    return wrapped_text

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    # Create a subdirectory for PDFs if it doesn't exist
    pdf_directory = os.path.join(os.getcwd(), 'pdfs')
    if not os.path.exists(pdf_directory):
        os.makedirs(pdf_directory)

    # Process form data
    length = request.form.get('length', type=int, default=100)
    random_text = ''.join(random.choices(string.ascii_lowercase + ' ', k=length))
    prompt = request.form.get('topics', default='')

    openai.api_key = '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'  
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    generated_text = response.choices[0].text.strip()

    # Generate PDF
    pdf_filename = 'generated_file.pdf'
    pdf_path = os.path.join(pdf_directory, pdf_filename)
    c = canvas.Canvas(pdf_path, pagesize=letter)

    # Define font properties
    font_name = "Helvetica"
    font_size = 12
    c.setFont(font_name, font_size)

    # Define margins and line height
    left_margin = 72
    top_margin = 720
    line_height = 14

    # Wrap the generated text
    max_width = 450  # Adjust as needed
    wrapped_text = wrap_text(generated_text, max_width, font_name, font_size)

    # Draw the wrapped text
    y_position = top_margin
    for line in wrapped_text:
        c.drawString(left_margin, y_position, line)
        y_position -= line_height

    # Draw the length below the text
    c.drawString(left_margin, y_position - 20, f"Length: {length}")  

    c.save()

    # Respond with the URL of the PDF
    pdf_url = url_for('get_pdf', filename=pdf_filename)
    return jsonify(success=True, pdf_url=pdf_url)

@app.route('/pdf/<filename>')
def get_pdf(filename):
    directory = os.path.join(os.getcwd(), 'pdfs')  # 
    file_path = os.path.join(directory, filename)
    if os.path.exists(file_path):
        return send_from_directory(directory, filename)
    else:
        return "File not found", 404

if __name__ == '__main__':
    app.debug = True
    app.run()
    
