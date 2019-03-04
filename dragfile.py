from flask import Flask, redirect, render_template, request, url_for
import os
from flask_bcrypt import check_password_hash
from flask import (Flask, g, flash, render_template, redirect, url_for,request,send_from_directory,
                   abort,session)
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user,)
from werkzeug.utils import secure_filename
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_sqlalchemy import SQLAlchemy
from peewee import *


DEBUG = True
PORT = 8000
HOST = 'localhost'


app = Flask(__name__)
app.config["DEBUG"] = True



comments = []


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("new.html", comments=comments)

    comments.append(request.form["contents"])
    return redirect(url_for('index'))


dropzone = Dropzone(app)
# Dropzone settings

app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
app.config['DROPZONE_REDIRECT_VIEW'] = 'results'
# Uploads settings
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB

app.config['SECRET_KEY'] = 'supersecretkeygoeshere'
...

@login_required
@app.route('/home', methods=['GET', 'POST'])
def home():
    # set session for image results
    if "file_urls" not in session:
        session['file_urls'] = []
    # list to hold our uploaded image urls
    file_urls = session['file_urls']
    # handle image upload from Dropzone
    if request.method == 'POST':
        file_obj = request.files
        for f in file_obj:
            file = request.files.get(f)

            # save the file with to our photos folder
            filename = photos.save(
                file,
                name=file.filename
            )
            # append image urls
            file_urls.append(photos.url(filename))

        session['file_urls'] = file_urls
        return "uploading..."
    # return dropzone template on GET request
    return render_template('test.html')



@login_required
@app.route('/results')
def results():
    # redirect to home if no images to display
    if "file_urls" not in session or session['file_urls'] == []:
        return redirect(url_for('home'))

    # set the file_urls and remove the session variable
    file_urls = session['file_urls']
    #session.pop('file_urls', None)
    return render_template('test.html', file_urls=file_urls)



#@app.route('/new')
#def new():
    #return render_template('new.html')






if __name__=="__main__":
    app.run(debug=DEBUG, host=HOST, port=PORT)