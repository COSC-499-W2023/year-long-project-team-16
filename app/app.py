import os
import re
import random
import string
from click import wrap_text
from flask import Flask, jsonify, render_template, request, send_from_directory, url_for
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from flask_cors import CORS
import openai 
import matplotlib.pyplot as plt
from io import BytesIO



app = Flask(__name__, template_folder='my_templates')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/content')
def content():
    return render_template('content.html')


@app.route('/settings.html')
def settings_html():
    return render_template('settings.html')


@app.route('/ai.html')
def ai_html():
    return render_template('ai.html')

def is_latex(text):
    """Check if the text is a LaTeX expression."""
    return bool(re.search(r"\$.*\$", text))

def render_latex(formula, fontsize=12, dpi=150):
    """Render LaTeX formula into an image."""
    # Configure Matplotlib to use LaTeX for rendering
    plt.rcParams['text.usetex'] = True
    
    # Set up a Matplotlib figure and text
    fig = plt.figure()
    fig.patch.set_alpha(0)
    ax = fig.add_subplot(111)
    ax.axis('off')
    ax.patch.set_alpha(0)
    # Use the formula within a TeX environment
    ax.text(0, 0, f"\\begin{{equation}}{formula}\\end{{equation}}", fontsize=fontsize)
    
    # Save the figure to a BytesIO buffer
    buffer = BytesIO()
    fig.savefig(buffer, dpi=dpi, transparent=True, format='png')
    plt.close(fig)
    buffer.seek(0)
    return buffer



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
    prompt = request.form.get('topics', default='')

    # Set OpenAI API key and get response
    openai.api_key = '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'  
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000
    )
    generated_text = response.choices[0].text.strip()

    # Define font properties and margins
    font_name = "Helvetica"
    font_size = 12
    left_margin = 72
    top_margin = 720
    line_height = 14

    # Generate PDF
    pdf_filename = 'generated_file.pdf'
    pdf_path = os.path.join(pdf_directory, pdf_filename)
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setFont(font_name, font_size)

    # Process the text
    parts = re.split(r"(\$.*?\$)", generated_text)
    y_position = top_margin

    for part in parts:
        if is_latex(part):
            latex_image_io = render_latex(part[1:-1])  # Remove $ symbols
            c.drawImage(latex_image_io, left_margin, y_position, width=200, height=100, preserveAspectRatio=True, anchor='n')
            y_position -= 100  # Adjust for image height
        else:
            wrapped_text = wrap_text(part, 450, font_name, font_size)
            for line in wrapped_text:
                c.drawString(left_margin, y_position, line)
                y_position -= line_height

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
    
