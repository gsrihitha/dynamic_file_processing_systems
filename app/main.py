import os
from flask import Flask, request # Required imports for web handling

#import graph based module that is defined with name processor as a sibling file
from .processing import process_with_graph # type: ignore

app = Flask(__name__) # Initializing the flask application

# Ensure we have an uploads/ folder next to app/
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads'))
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    '''Render a simple HTML form.
    -method POST: form uses HTTP POST (POST is typically used when the client needs to submit data that will result in a change of state on the server (e.g., creating a new resource, submitting a form, uploading a file) rather than merely retrieving existing data )
    - enctype multipart/formdata: This enables uploads of files'''
    
    return '''
    <h1>Upload File</h1>
    <form method="POST" action="/upload" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload & Process">
    </form>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():

    '''
    This is done to handle file upload, processing, and return summary.
    Steps involved:
        1) Validate Request for the file part
        2) Save uploaded files in a disk
        3) Invoke processing pipeline
        4) Return summary with HTML line breaks
    '''

    # 1) Did the browser send a multipart file part?
    # Ensure if the 'file' part exists in the request
    if 'file' not in request.files:
        return "No file part in request. Did you set enctype?", 400

    file = request.files['file']
    # 2) Did they actually select a file or a non-empty file?
    if file.filename == '':
        return "No file selected.", 400

    # 3) Save the uploaded file
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(save_path)

    # 4) Wire in your graph-based pipeline
    summary = process_with_graph(file.filename)

    # 5) Return HTML—replace newlines with <br> so the browser shows line breaks
    return summary.replace('\n', '<br>')

if __name__ == '__main__':
    app.run(debug=True) #Run the flask development server with the debug mode on









