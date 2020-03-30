from flask import Flask, render_template, request
from werkzeug import secure_filename
import os

""" Modified from https://github.com/twtrubiks/flask-dropzone-wavesurfer"""

uploadfiles = Flask(__name__)
UPLOAD_PATH = 'static/uploads'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_PATH)
UPLOAD_F = os.path.abspath(os.path.join(APP_ROOT, os.pardir))

#TODO: Handle VagrantFiles, VMs, exploits (zip, 7z, etc.) or just everything?
#TODO: get existing files??
#TODO: Set appropiate paths to files. 
#TODO: See what the scope of what I need to do is.

@uploadfiles.route('/')
def index():
    all_VMs = []
    all_exploits = []
    all_vagrantfiles = []
    all_image_files = []
    for filename in os.listdir(UPLOAD_FOLDER):
        ## Check for VMs
        if (isVMFormat(filename)):
            all_VMs.append(filename)
        ## Exploits
        if (isExploitFormat(filename)):
            all_exploits.append(filename)
        ## VagrantFiles
        if (isVagrantFileFormat(filename)):
            all_vagrantfiles.append(filename)
            
        if (filename.find('.png') > -1):
            all_image_files.append(filename)
            
    return render_template('index.html', **locals());


def isVMFormat(link):
    if (link.find('.ova') > -1):
        return True;
    return False;

def isExploitFormat(link):
    if (link.find('.txt') > -1 or link.find('.go') > -1 or link.find('.py') > -1):
        return True;
    return False;

#TODO: This method
def isVagrantFileFormat(link):
    if (link.find('.png') > -1):
        return True;
    return False;

@uploadfiles.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        upload_path = '{}/{}'.format(UPLOAD_FOLDER, secure_filename(file.filename))
        print(UPLOAD_FOLDER)
        file.save(upload_path)
        return 'ok'


if __name__ == '__main__':
    uploadfiles.run(debug=False)
