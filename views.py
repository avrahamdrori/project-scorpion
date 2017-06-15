from flask import Flask, render_template, request, flash,g,session,url_for, send_file
from models import *
from sendmail import *
import uuid
import os, sys
from os import curdir, sep
from PyQt4.Qt import flush
from django.core.mail import send_mail
from qrgen import *
from fileinput import filename
from flask.helpers import send_from_directory
import shutil
from shutil import copyfile
app = Flask(__name__, static_url_path='')
upload_path = os.path.join(os.curdir,'files')

@app.route('/', methods=['GET', 'POST'])
def mainNew():
    error = ''
    if request.method == 'POST':

        newfilename = uuid.uuid1()
        if 'upfile' not in request.files:
            error='no file'
            print error
            return render_template('upload.template.html', error=error)
        f = request.files['upfile']
        email = request.form.get('Email')
#         flush( f.filename)
        originalFileName = f.filename.encode()
        uuidName = newfilename
        numOfTimes = request.form.get('downNum')
        newfilepath=os.path.join(upload_path, str(newfilename))
        f.save(newfilepath)
#         print(email)
        insert_file(email,originalFileName,uuidName.__str__(),numOfTimes)
#         send_mail('fridgeMaster@filefridge.com', email, 'Your file was uploaded succefully to FileFrige', 'To take your file out of the fridge. To Take it out follow this link <a href="http://localhost:5000/files/</a>+uuidName.encode())
        error='file ' + originalFileName + ' was uploaded successfully'
        make_qr(uuidName)
        return render_template('upload.template.html', error=error, uuidName=uuidName)
    else:
        return render_template('upload.template.html',error=error)
    
@app.route('/user', methods=['GET', 'POST'])
def userpage():
    if request.method == 'POST':
        email = request.form.get('Email').encode()
        rows=getFileList(email)
        print rows
        return render_template('files.template.html', rows=rows,email=email)
    return render_template('user.template.html')
# @app.route('/uuidImages<path:filename>')
# def show_image(filename):
#     return send_from_directory('uuidImages',filename)
@app.route('/download/<fileuuid>')
def dlFile(fileuuid):
    Ofilename=getFilenamyByUuid(fileuuid)
    copyfile("files/"+fileuuid.encode(),"static/tmp/"+Ofilename[0])
    return send_file('static/tmp/' + Ofilename[0])