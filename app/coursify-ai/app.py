from datetime import datetime
import os
import re
import random
import string
from click import wrap_text
from flask import Flask, jsonify, render_template, request, send_from_directory, url_for, Response, send_file, make_response
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from flask_cors import CORS
import openai 
import matplotlib.pyplot as plt
from io import BytesIO
from pymongo import MongoClient
from gridfs import GridFS
from PyPDF2 import PdfReader
from werkzeug.utils import secure_filename
from flask_mail import Mail,Message
from bson.objectid import ObjectId



app = Flask(__name__, template_folder='my_templates')
CORS(app)

app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com' #we use outlook because gmail was wasting time
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True 
app.config['MAIL_USERNAME'] = 'coursify@outlook.com'  
app.config['MAIL_PASSWORD'] = 'Gunners4Eva.' 

mail = Mail(app)

# Setup MongoDB connection
client = MongoClient('mongodb+srv://Remy:1234@cluster0.vgzdbrr.mongodb.net/')
db = client['generated_pdfs']
fs = GridFS(db)

@app.route('/share/<file_id>')
def share_file(file_id):
    # converts id to objectid
    file_id = ObjectId(file_id)

    # Retrieve the file from GridFS
    file = fs.get(file_id)

    # Create a response with the file data
    response = make_response(file.read())
    response.mimetype = 'application/pdf'

    # Set the Content-Disposition header to make the file downloadable
    response.headers.set('Content-Disposition', 'attachment', filename=file.filename)

    return response


def extract_text_from_pdf(pdf_path):
    # This function extracts text from a PDF using PdfReader
    with open(pdf_path, 'rb') as f:
        reader = PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

@app.route('/content')
def my_content():
    # Get a list of all files in GridFS
    files = fs.find()

    # Create a list to store file data
    file_data = []

    # Loop through all files
    for file in files:
        # Get the file name and the file id (used to retrieve the file later)
        file_data.append({"filename": file.filename, "_id": str(file._id)})

    # Render a template and pass the file data to it
    return render_template('content.html', file_data=file_data)

@app.route('/share_via_email', methods=['POST'])
def share_via_email():
    # Get the recipient's email address and the file id from the form data
    recipient = request.form.get('email')
    file_id = request.form.get('file_id')

    # Generate the shareable URL
    share_url = url_for('share_file', file_id=file_id, _external=True)

    # Create a new email message
    msg = Message('Your Shared File',
                  sender='coursify@outlook.com',
                  recipients=[recipient])

    # Add the shareable URL to the email body
    msg.body = f'Here is the file you requested: {share_url}'

    # Send the email
    mail.send(msg)

    return 'Email sent!' 

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

    return bool(re.search(r"\$.*\$", text))

def render_latex(formula, fontsize=12, dpi=150):

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


def sanitize_filename(text):
    # Remove invalid filename characters
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    sanitized = ''.join(c for c in text if c in valid_chars)
    # Truncate the filename if it's too long
    return sanitized[:255]


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
    difficulty = request.form.get('difficulty',default='')

    # Process optional PDF upload
    pdf_upload = request.files.get('pdf-upload')
    uploaded_text = ""

    if pdf_upload and pdf_upload.filename:
        pdf_path = os.path.join(pdf_directory, secure_filename(pdf_upload.filename))
        pdf_upload.save(pdf_path)
        uploaded_text = extract_text_from_pdf(pdf_path)

        # Combine uploaded text with user's topics
    combined_prompt = uploaded_text + "\n" + prompt

    pdf_basename = sanitize_filename(combined_prompt)

    # Ensure the filename is not empty
    pdf_basename = pdf_basename if pdf_basename else 'generated_file'

    # Add a timestamp or random string to the filename to ensure uniqueness
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    unique_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    pdf_filename = f"{pdf_basename}_{timestamp}_{unique_suffix}.pdf"

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
    
     # Save the PDF to MongoDB
    with open(pdf_path, 'rb') as f:
        fs.put(f, filename=pdf_filename, content_type='application/pdf')


    # Respond with the URL of the PDF
    pdf_url = url_for('get_pdf', filename=pdf_filename)
    return jsonify(success=True, pdf_url=pdf_url)


@app.route('/pdf/<filename>')
def get_pdf(filename):
     directory = os.path.join(os.getcwd(), 'pdfs')   
     file_path = os.path.join(directory, filename)
     if os.path.exists(file_path):
         return send_from_directory(directory, filename)
     else:
         return "File not found", 404

    
  
  #can be used to check if file is in database  
@app.route('/check_file/<filename>', methods=['GET'])
def check_file(filename):
    try:
        file = fs.get_last_version(filename=filename)
        if file:
            return jsonify(success=True, message="File exists in the database.")
    except:
        return jsonify(success=False, message="File does not exist in the database.")
    

@app.route("/chatbot", methods=["POST"])
def chatbot():
    # Get the message from the POST request
    message = request.json.get("message")

    # Set OpenAI API key (if not already set globally)
    openai.api_key = 'your-api-key'

    # Send the message to OpenAI's API and receive the response
    completion = openai.Completion.create(
        engine="text-davinci-003",  # Use the text-davinci-003 model
        prompt=message,
        max_tokens=150  # Adjust max_tokens if necessary
    )

    if completion.choices and completion.choices[0].text.strip() != "":
        return completion.choices[0].text.strip()
    else:
        return 'Failed to Generate response!'
    
   
    
if __name__ == '__main__':
    app.debug = True
    app.run()
    
