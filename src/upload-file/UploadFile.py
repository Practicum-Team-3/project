# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 21:55:57 2020

@author: revil0mg
"""

# coding:utf-8

from flask import Flask,render_template,request,redirect,url_for
from werkzeug.utils import secure_filename
import os
from time import sleep
from flask import copy_current_request_context
import threading
import datetime

app = Flask(__name__)

@app.route('/upload', methods=['POST','GET'])
def upload():
    @copy_current_request_context
    def save_file(closeAfterWrite):
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " i am doing")
        f = request.files['file']
        basepath = os.path.dirname(__file__) 
        upload_path = os.path.join(basepath, '',secure_filename(f.filename)) 
        f.save(upload_path)
        closeAfterWrite()
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " write done")
        
    def passExit():
        pass
    
    if request.method == 'POST':
        f= request.files['file']
        normalExit = f.stream.close
        f.stream.close = passExit
        t = threading.Thread(target=save_file,args=(normalExit,))
        t.start()
        return redirect(url_for('upload'))
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)