from flask import Flask, render_template, request
from werkzeug import secure_filename
import os

""" Modified from https://github.com/twtrubiks/flask-dropzone-wavesurfer"""

app = Flask(__name__)
UPLOAD_PATH = 'static/uploads'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_PATH)

#TODO: Handle VagrantFiles, VMs, exploits (zip, 7z, etc.) or just everything?
#TODO: get existing files??
#TODO: Set appropiate paths to files. 
#TODO: See what the scope of what I need to do is.

@app.route('/')
def index():
    all_VMs = []
    all_mp3_files = []
    for filename in os.listdir(UPLOAD_FOLDER):
        ## Check for VMs
        if (isVMFormat(filename)):
            all_VMs.append(filename)
        ## mp3
        if (filename.find('.mp3') > -1):
            all_mp3_files.append(filename)
    return render_template('index.html', **locals());


# 符合圖片檔案
def isVMFormat(link):
    if (link.find('.ova') > -1):
        return True;
    return False;


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        upload_path = '{}/{}'.format(UPLOAD_FOLDER, file.filename)
        file.save(upload_path)
        return 'ok'


if __name__ == '__main__':
    app.run(debug=False)
