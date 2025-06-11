from flask import Flask, request

#unused for now- render_template, request, redirect, url_for

# flask is the core class
# render_template a helper function to render HTML Files stores in templates/ folder
# request - gives you access to incoming HTTP data - form data, file uploads, query parameters etc.
# redirect and url_for - helps redirect users to a different route

import os 
# builtin interface - helps you work with folders files and paths



def my_func():
    # pylint: disable=missing-docstring
    pass

app = Flask(__name__)

# instantiating a new Flask application object - app
# here the __name__ tells flask where to look for templates, and static files, use it to know the root of the project.

UPLOAD_FOLDER = '../uploads'
# A path to store the uploaded files
# ../uploads works if:
'''
file-processing-system/
├─ app/main.py
├─ uploads/
'''

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# This ensures that forlder exists, and exist_ok = True ensures not to throw an error if the file already exists
# Creates new file if it does't exist

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Stores path in Flask's comfiguration dictionary, so that it can be referred in multiple places as app.config['UPLOAD_FOLDER']

''' Home-page '''
@app.route('/')
#This is a decorator that tells flask that if somebody visits the URL path /, run the function immediately below:

def index():
    return '''
    <h1> Upload Files </h1>
    <form method = "POST" action = "/upload" enctype = "multi[art/form-data"
        <input type = "file" name = "file">
        <input type = "submit" value = "Upload">
    </form>
    '''
# The function above sends a raw HTML string containing:
# A heading
# A form with with method - form data will be sent using HTTP POST, action where the browser will send the form to upload URL, enctype - tells browser to package file data correctly
# Note - enctype - is encode type 
# for input: a file picker control named file 
# A submit button that does upload

# method to handle file upload (runs after the form is submitted):
@app.route('/upload', methods = ['POST'])
def upload_file():
    file = request.files['file']
    # is a dictionary of all uploaded files, we access the one whose form field is named file
    if file: #Checks if a file is not empty
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        # Builds a safe path by combining the upload folder and the original name (eg: upload_folder is report, filename: pdf)
        file.save(filepath)
        # saves the uploaded files binary data to the path you specified
        return f"File '{file.filename}' uploaded successfully!" # Confirmation
    return "No file selected" # If file not uploaded

if __name__ == '__main__': # Ensures that this block only runs when you execute this file directly, and not when you import it as a module elsewhere
    app.run(debug=True) 
    # app.run starts flasks built-in development web server on localhost
    # debug = true enables hot reload, so that server automatically restarts when you change code, also shows errors



