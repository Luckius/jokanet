import os
import secrets
import datetime
from flask_socketio import SocketIO,send,disconnect
from flask_bcrypt import check_password_hash
from flask import (Flask, g, flash, render_template, redirect, url_for,request,send_from_directory,
                   abort,session)
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user,)
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,TextAreaField,SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import (DataRequired, Regexp, ValidationError,Email,
                                Length, EqualTo,)
from flask_wtf import Form
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
import functools
from forms import MusicSearchForm


import forms
import models
import sys

app = Flask(__name__)



dropzone = Dropzone(app)
# Dropzone settings
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
app.config['DROPZONE_REDIRECT_VIEW'] = 'forums'
# Uploads settings
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB

app.config['SECRET_KEY'] = 'luckiusevodiuskajokarutakararwagojobaomuhaya'





DEBUG = True
PORT = 8000
HOST = 'localhost'


app.secret_key = 'auoesh,jahskd,alkjds,k_swekdius'

login_manager =LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None



@app.before_request
def before_request():
    """connect to the data base before each request"""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """close to the data base each after request"""
    g.db.close()
    return response


@app.route('/jokamedia')
def jokamedia():
    return render_template('jokamedia.html')


@app.route('/about')
def about():
    return render_template('about.html')




@app.route('/allusers')
def allusers():
    allusers = models.User.select().order_by(models.User.id.desc())
    return render_template('active.html',allusers=allusers)




@app.route('/register', methods = ('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Wow you registered wellcome, please login to start chating with members " , "success")
        myuser=models.User.create_user(
                      username=form.username.data,
                      email=form.email.data,
                      password=form.password.data,
        )
        models.FTSUser.create(docid=myuser.id,content='\n'.join(myuser.username))
        return redirect(url_for('login'))
    return render_template('register.html', form = form)






@app.route('/login', methods = ('GET', 'POST'))
def login():
    form=forms.LoginForm()
    if form.validate_on_submit():
        try:
            user=models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("mach your email or password","error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("you have been logged in", "success")
                return redirect(url_for('index'))
            else:
                flash("your email or password doesn't match", "error")
    return render_template('login.html',form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("you have been logged out come back soon", "success")
    return redirect(url_for('jokamedia'))


@app.route('/new_post', methods = ('GET', 'POST'))
@login_required
def post():
    form = forms.PostForm()
    if form.validate_on_submit():
        models.Post.create(user=g.user._get_current_object(),content= form.content.data.strip())
        flash("Message posted! Thanks!", "success")
        return redirect(url_for('index'))
    return render_template('post.html', form=form)



@app.route('/new_message', methods = ('GET', 'POST'))
@login_required
def message():
    form = forms.MessageForm()
    if form.validate_on_submit():
        models.Message.create(user=g.user._get_current_object(),content= form.content.data.strip())
        flash("Message done! Thanks!", "success")
        return redirect(url_for('my_message'))
    return render_template('message.html', form=form)


@app.route('/photo_message', methods = ('GET', 'POST'))
@login_required
def photo_message():
    form = forms.PhotomessageForm()
    if form.validate_on_submit():
        models.Photomessage.create(user=g.user._get_current_object(),content= form.content.data.strip())
        flash("Message aded! Thanks!", "success")
        return redirect(url_for('results'))
    return render_template('photomessage.html', form=form)




@app.route('/ourgamesimage_msg', methods = ('GET', 'POST'))
@login_required
def ourgamesimage_msg():
    form = forms.GamesmsgForm()
    if form.validate_on_submit():
        models.Gamesmsg.create(user=g.user._get_current_object(),content= form.content.data.strip())
        flash("Message aded! Thanks!", "success")
        return redirect(url_for('ourgames'))
    return render_template('gamesmsg.html', form=form)




@app.route('/oursportsimage_msg', methods = ('GET', 'POST'))
@login_required
def oursportsimage_msg():
    form = forms.SportsmsgForm()
    if form.validate_on_submit():
        models.Sportsmsg.create(user=g.user._get_current_object(),content= form.content.data.strip())
        flash("Message aded! Thanks!", "success")
        return redirect(url_for('oursports'))
    return render_template('sportsmsg.html', form=form)


@app.route('/ourbussnesimage_msg', methods = ('GET', 'POST'))
@login_required
def ourbussnesimage_msg():
    form = forms.BussnesmsgForm()
    if form.validate_on_submit():
        models.Bussnesmsg.create(user=g.user._get_current_object(),content= form.content.data.strip())
        flash("Message aded! Thanks!", "success")
        return redirect(url_for('ourbussnes'))
    return render_template('bussnesmsg.html', form=form)



@app.route('/ourpolitcsimage_msg', methods = ('GET', 'POST'))
@login_required
def ourpolitcsimage_msg():
    form = forms.PolitcsmsgForm()
    if form.validate_on_submit():
        models.Politcsmsg.create(user=g.user._get_current_object(),content= form.content.data.strip())
        flash("Message aded! Thanks!", "success")
        return redirect(url_for('ourpolitcs'))
    return render_template('politcsmsg.html', form=form)





@login_required
@app.route('/my_message')
def my_message():
    message_stream = models.Message.select().where(models.Message.user.in_(current_user.following()))
    #message_stream = models.Message.select().where(models.Message.user << models.User.following())
    return render_template('result_uploads.html', message_stream=message_stream)



@login_required
@app.route('/our_images')
def our_images():
    images_stream = models.Images.select().where(models.Images.user.in_(current_user.following()))
    #message_stream = models.Message.select().where(models.Message.user << models.User.following())
    return render_template('show_image.html', images_stream=images_stream)


@login_required
@app.route('/my_album')
def my_album():
    my_albums = models.Images.select().where(models.Images.user.in_(current_user.following()))
    #message_stream = models.Message.select().where(models.Message.user << models.User.following())
    return render_template('my_album.html', my_albums=my_albums)




@app.route('/')
@login_required
def index():
    stream = models.Post.select().order_by(models.Post.id.desc())
    return render_template('stream.html', stream=stream)




@login_required
@app.route('/stream')
@app.route('/stream/<username>')
def stream(username=None):
    template = 'stream.html'
    if username and username != current_user.username:
        try:
            user = models.User.select().where(models.User.username**username).get()
        except models.DoesNotExist:
            abort(404)
        else:
            stream = user.posts.limit(100)
    else:
        stream = current_user.get_stream().limit(100)
        user=current_user
    if username:
        template='user_stream.html'
    return render_template(template,stream=stream, user=user)



#clasify stand like stream but clasfy just clasify the comment on photo
@login_required
@app.route('/message_stream')
@app.route('/message_stream/<username>')
def message_stream(username=None):
    template = 'result_uploads.html'
    if username and username != current_user.username:
        try:
            user = models.User.select().where(models.User.username**username).get()
            #user = models.User.select().where(models.User.username << username).get()
        except models.DoesNotExist:
            abort(404)
        else:
            message_stream = user.messages.limit(100)
    else:
        message_stream = current_user.get_message_stream().limit(100)
        user=current_user
    if username:
        template = 'user_clasify.html'
    return render_template(template,message_stream=message_stream, user=user)


@login_required
@app.route('/commment_stream')
@app.route('/comment_stream/<username>')
def comment_stream(username=None):
    template = 'new.html'
    if username and username != current_user.username:
        try:
            user = models.User.select().where(models.User.username**username).get()
            #user = models.User.select().where(models.User.username << username).get()
        except models.DoesNotExist:
            abort(404)
        else:
            comment_stream = user.comments.limit(1000)
    else:
        comment_stream = current_user.get_comment_stream().limit(100)
        user=current_user
    if username:
        template = 'user_clasify.html'
    return render_template(template,comment_stream=comment_stream, user=user)


@login_required
@app.route('/images_stream')
@app.route('/images_stream/<username>')
def images_stream(username=None):
    template = 'show_image.html'
    if username and username != current_user.username:
        try:
            user = models.User.select().where(models.User.username**username).get()
            #user = models.User.select().where(models.User.username << username).get()
        except models.DoesNotExist:
            abort(404)
        else:
            images_stream = user.images.limit(1000)
    else:
        images_stream = current_user.get_images_stream().limit(100)
        user=current_user
    if username:
        template = 'user_stream.html'
    return render_template(template,images_stream=images_stream, user=user)



@login_required
@app.route('/drphoto_stream')
@app.route('/drphoto_stream/<username>')
def drphoto_stream(username=None):
    template = 'dropzone.html'
    if username and username != current_user.username:
        try:
            user = models.User.select().where(models.User.username**username).get()
            #user = models.User.select().where(models.User.username << username).get()
        except models.DoesNotExist:
            abort(404)
        else:
            drphoto_stream = user.drphotos.limit(1000)
    else:
        drphoto_stream = current_user.get_drphoto_stream().limit(100)
        user=current_user
    if username:
        template = 'user_stream.html'
    return render_template(template,drphoto_stream=drphoto_stream, user=user)



@login_required
@app.route('/ourgamesimage_stream')
@app.route('/ourgamesimage_stream/<username>')
def ourgamesimage_stream(username=None):
    template = 'dropzone.html'
    if username and username != current_user.username:
        try:
            user = models.User.select().where(models.User.username**username).get()
            #user = models.User.select().where(models.User.username << username).get()
        except models.DoesNotExist:
            abort(404)
        else:
            ourgamesimage_stream = user.ourgamesimages.limit(1000)
    else:
        drphoto_stream = current_user.get_ourgamesimage_stream().limit(100)
        user=current_user
    if username:
        template = 'user_stream.html'
    return render_template(template,ourgamesimage_stream=ourgamesimage_stream, user=user)



@login_required
@app.route('/oursportsimage_stream')
@app.route('/oursportsimage_stream/<username>')
def oursportsimage_stream(username=None):
    template = 'dropsports.html'
    if username and username != current_user.username:
        try:
            user = models.User.select().where(models.User.username**username).get()
            #user = models.User.select().where(models.User.username << username).get()
        except models.DoesNotExist:
            abort(404)
        else:
            oursportsimage_stream = user.oursportsimages.limit(1000)
    else:
        drphoto_stream = current_user.get_oursportsimage_stream().limit(100)
        user=current_user
    if username:
        template = 'user_stream.html'
    return render_template(template,oursportsimage_stream=oursportsimage_stream, user=user)


@login_required
@app.route('/ourbussnesimage_stream')
@app.route('/ourbussnesimage_stream/<username>')
def ourbussnesimage_stream(username=None):
    template = 'dropbussnes.html'
    if username and username != current_user.username:
        try:
            user = models.User.select().where(models.User.username**username).get()
            #user = models.User.select().where(models.User.username << username).get()
        except models.DoesNotExist:
            abort(404)
        else:
            ourbussnesimage_stream = user.ourbussnessimages.limit(1000)
    else:
        drphoto_stream = current_user.get_ourbussnesimage_stream().limit(100)
        user=current_user
    if username:
        template = 'user_stream.html'
    return render_template(template,ourbussnesimage_stream=ourbussnesimage_stream, user=user)


@login_required
@app.route('/ourpolitcsimage_stream')
@app.route('/ourpolitcsimage_stream/<username>')
def ourpolitcsimage_stream(username=None):
    template = 'droppolitcs.html'
    if username and username != current_user.username:
        try:
            user = models.User.select().where(models.User.username**username).get()
            #user = models.User.select().where(models.User.username << username).get()
        except models.DoesNotExist:
            abort(404)
        else:
            ourpolitcsimage_stream = user.ourpolitcsimages.limit(1000)
    else:
        drphoto_stream = current_user.get_ourpolitcsimage_stream().limit(100)
        user=current_user
    if username:
        template = 'user_stream.html'
    return render_template(template,ourpolitcsimage_stream=ourpolitcsimage_stream, user=user)




@login_required
@app.route('/photomessage_stream')
@app.route('/photomessage_stream/<username>')
def photomessage_stream(username=None):
    template = 'dropzone.html'
    if username and username != current_user.username:
        try:
            user = models.User.select().where(models.User.username**username).get()
            #user = models.User.select().where(models.User.username << username).get()
        except models.DoesNotExist:
            abort(404)
        else:
            photomessage_stream = user.photomessages.limit(100)
    else:
        photomessage_stream = current_user.get_photomessage_stream().limit(100)
        user=current_user
    if username:
        template = 'user_clasify.html'
    return render_template(template,photomessage_stream=photomessage_stream, user=user)




@login_required
@app.route('/ourgamesmsg_stream')
@app.route('/ourgamesmsg_stream/<username>')
def ourgamesmsg_stream(username=None):
    template = 'dropzone.html'
    if username and username != current_user.username:
        try:
            user = models.User.select().where(models.User.username**username).get()
            #user = models.User.select().where(models.User.username << username).get()
        except models.DoesNotExist:
            abort(404)
        else:
            ourgamesmsg_stream = user.ourgamesmsgs.limit(100)
    else:
        ourgamesmsg_stream = current_user.get_ourgamesmsg_stream().limit(100)
        user=current_user
    if username:
        template = 'user_clasify.html'
    return render_template(template,ourgamesmsg_stream=ourgamesmsg_stream, user=user)




@login_required
@app.route('/ourbussnesmsg_stream')
@app.route('/ourbussnesmsg_stream/<username>')
def ourbussnesmsg_stream(username=None):
    template = 'dropzone.html'
    if username and username != current_user.username:
        try:
            user = models.User.select().where(models.User.username**username).get()
            #user = models.User.select().where(models.User.username << username).get()
        except models.DoesNotExist:
            abort(404)
        else:
            ourbussnesmsg_stream = user.ourbussnesmsgs.limit(100)
    else:
        ourbussnesmsg_stream = current_user.get_ourbussnesmsg_stream().limit(100)
        user=current_user
    if username:
        template = 'user_clasify.html'
    return render_template(template,ourbussnesmsg_stream=ourbussnesmsg_stream, user=user)



@login_required
@app.route('/ourpolitcsmsg_stream')
@app.route('/ourpolitcsmsg_stream/<username>')
def ourpolitcsmsg_stream(username=None):
    template = 'dropzone.html'
    if username and username != current_user.username:
        try:
            user = models.User.select().where(models.User.username**username).get()
            #user = models.User.select().where(models.User.username << username).get()
        except models.DoesNotExist:
            abort(404)
        else:
            ourpolitcsmsg_stream = user.ourpolitcsmsgs.limit(100)
    else:
        ourpolitcsmsg_stream = current_user.get_ourpolitcsmsg_stream().limit(100)
        user=current_user
    if username:
        template = 'user_clasify.html'
    return render_template(template,ourpolitcsmsg_stream=ourpolitcsmsg_stream, user=user)




@login_required
@app.route('/post/<int:post_id>')
def view_post(post_id):
    posts = models.Post.select().where(models.Post.id == post_id)
    return render_template('stream.html', stream=posts)





@app.route('/follow/<username>')
@login_required
def follow(username):
    try:
        to_user = models.User.get(models.User.username**username)
    except models.DoesNotExist:
        abort(404)
    else:
        try:
            models.Relationship.create(
                from_user = g.user._get_current_object(),
                to_user = to_user
            )
        except models.IntegrityError:
            pass
        else:
            if to_user.username == current_user.username:
                flash("Now you can see your private post with your followers", "success")
            else:
                flash("you are now following {}!".format(to_user.username), "success")
    return redirect(url_for('stream', username=to_user.username))


@app.route('/unfollow<username>')
@login_required
def unfollow(username):
    try:
        to_user =models.User.get(models.User.username**username)
    except models.DoesNotExist:
        abort(404)
    else:
        try:
            models.Relationship.get(
                from_user = g.user._get_current_object(),
                to_user = to_user
            ).delete_instance()
        except models.IntegrityError:
            pass
        else:
            flash("you have unfollowed {}".format(to_user.username), "success")
    return redirect(url_for('stream',username=to_user.username))

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404


#deleting posts
@app.route('/delete_post/<int:post_id>')
@login_required
def delete_post(post_id):
    try:
        my_post = models.Post.select().where(models.Post.id == post_id).get()
        #post = models.Post.delete().where((models.Post.timestamp) >
                                          #(datetime.date.today() - datetime.timedelta(days=7)))
    except models.Post.DoesNotExist:
        abort(404)
    my_post.delete_instance()
    #post.execute()
    flash("This post has successfully been deleted.", "success")
    return redirect(url_for('stream', stream=stream))


#deleting posts
@app.route('/delete_message/<int:message_id>')
@login_required
def delete_message(message_id):
    try:
        my_message = models.Message.select().where(models.Message.id == message_id).get()
        #post = models.Post.delete().where((models.Post.timestamp) >
                                          #(datetime.date.today() - datetime.timedelta(days=7)))
    except models.Message.DoesNotExist:
        abort(404)
    my_message.delete_instance()
    #post.execute()
    flash("This message has successfully been deleted.", "success")
    return redirect(url_for('message_stream', message_stream=message_stream))





@app.route('/delete_lastpost')
@login_required
def delete_lastpost():
    try:
        post = models.Post.delete().where(
            (models.Post.timestamp) > (datetime.date.today() - datetime.timedelta(minutes=1)))
    except models.Post.DoesNotExist:
        abort(404)
    post.execute()

    flash("posts more than one week has been deleted.", "success")
    return redirect(url_for('stream', stream=stream))



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
            for url in file_urls:
                models.Drphoto.create(user=g.user._get_current_object(), filename=filename, fp=url)

        session['file_urls'] = file_urls
        return "uploading..."
    # return dropzone template on GET request
    return render_template('dropzonearea.html')



@login_required
@app.route('/forums')
def forums():
    return render_template('forums.html')





@login_required
@app.route('/results')
def results():
    # redirect to home if no images to display
    '''if "file_urls" not in session or session['file_urls'] == []:
        return redirect(url_for('home'))
    # set the file_urls and remove the session variable
    file_urls = session['file_urls']'''


    photomessage_stream = models.Photomessage.select().limit(1)
    drphoto_stream = models.Drphoto.select().limit(1)
    session.pop('file_urls', None)
    return render_template('dropzone.html', drphoto_stream=drphoto_stream,photomessage_stream=photomessage_stream)





@login_required
@app.route('/games', methods=['GET', 'POST'])
def games():
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
            for url in file_urls:
                models.Gamesimage.create(user=g.user._get_current_object(), filename=filename, fp=url)

        session['file_urls'] = file_urls
        return "uploading..."
    # return dropzone template on GET request
    return render_template('dropzonegames.html')



@login_required
@app.route('/ourgames')
def ourgames():
    # redirect to home if no images to display
    '''if "file_urls" not in session or session['file_urls'] == []:
        return redirect(url_for('home'))
    # set the file_urls and remove the session variable
    file_urls = session['file_urls']'''


    ourgamesmsg_stream = models.Gamesmsg.select().limit(1)
    ourgamesimage_stream = models.Gamesimage.select().limit(1)
    session.pop('file_urls', None)
    return render_template('dropgames.html', ourgamesimage_stream=ourgamesimage_stream,
                            ourgamesmsg_stream=ourgamesmsg_stream)



@login_required
@app.route('/sports', methods=['GET', 'POST'])
def sports():
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
            for url in file_urls:
                models.Sportsimage.create(user=g.user._get_current_object(), filename=filename, fp=url)

        session['file_urls'] = file_urls
        return "uploading..."
    # return dropzone template on GET request
    return render_template('dropzonesports.html')



@login_required
@app.route('/oursports')
def oursports():
    # redirect to home if no images to display
    '''if "file_urls" not in session or session['file_urls'] == []:
        return redirect(url_for('home'))
    # set the file_urls and remove the session variable
    file_urls = session['file_urls']'''


    oursportsmsg_stream = models.Sportsmsg.select().limit(1)
    oursportsimage_stream = models.Sportsimage.select().limit(1)
    session.pop('file_urls', None)
    return render_template('dropsports.html', oursportsimage_stream=oursportsimage_stream,
                            oursportsmsg_stream=oursportsmsg_stream)




@login_required
@app.route('/bussnes', methods=['GET', 'POST'])
def bussnes():
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
            for url in file_urls:
                models.Bussnesimage.create(user=g.user._get_current_object(), filename=filename, fp=url)

        session['file_urls'] = file_urls
        return "uploading..."
    # return dropzone template on GET request
    return render_template('dropzonebussnes.html')



@login_required
@app.route('/ourbussnes')
def ourbussnes():
    # redirect to home if no images to display
    '''if "file_urls" not in session or session['file_urls'] == []:
        return redirect(url_for('home'))
    # set the file_urls and remove the session variable
    file_urls = session['file_urls']'''


    ourbussnesmsg_stream = models.Bussnesmsg.select().limit(1)
    ourbussnesimage_stream = models.Bussnesimage.select().limit(1)
    session.pop('file_urls', None)
    return render_template('dropbussnes.html', ourbussnesimage_stream=ourbussnesimage_stream,
                            ourbussnesmsg_stream=ourbussnesmsg_stream)





@login_required
@app.route('/politcs', methods=['GET', 'POST'])
def politcs():
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
            for url in file_urls:
                models.Politcsimages.create(user=g.user._get_current_object(), filename=filename, fp=url)

        session['file_urls'] = file_urls
        return "uploading..."
    # return dropzone template on GET request
    return render_template('dropzonepolitcs.html')



@login_required
@app.route('/ourpolitcs')
def ourpolitcs():
    # redirect to home if no images to display
    '''if "file_urls" not in session or session['file_urls'] == []:
        return redirect(url_for('home'))
    # set the file_urls and remove the session variable
    file_urls = session['file_urls']'''


    ourpolitcsmsg_stream = models.Politcsmsg.select().limit(1)
    ourpolitcsimage_stream = models.Politcsimages.select().limit(1)
    session.pop('file_urls', None)
    return render_template('droppolitcs.html', ourpolitcsimage_stream=ourpolitcsimage_stream,
                            ourpolitcsmsg_stream=ourpolitcsmsg_stream)




#my album
#form for photo posting
class UploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, u'Image only!'), FileRequired(u'File was empty!')])
    submit = SubmitField(u'Upload')



@login_required
@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = photos.url(filename)
        new_file = file_url
        models.Images.create(user=g.user._get_current_object(), filename=filename, fp=new_file )
        return redirect(url_for('my_album'))
    else:
        file_url = None
    return render_template('accounts.html', form=form)




#comment
@login_required
@app.route('/educationcmt', methods=["GET", "POST"])
def educationcmt():
    if request.method == "GET":
        commented = models.Comment.select().limit(1000)
        return render_template("new.html",commented=commented)
    models.Comment.create(user=g.user._get_current_object(), content=request.form["contents"])
    #comments = models.Comment(content=request.form["contents"])
    return redirect(url_for('educationcmt'))




#comment
@login_required
@app.route('/gamescmt', methods=["GET", "POST"])
def gamescmt():
    if request.method == "GET":
        gamescmtd = models.Gamescmtd.select().limit(100)
        return render_template("gamescmt.html",gamescmtd=gamescmtd)
    models.Gamescmtd.create(user=g.user._get_current_object(), content=request.form["contents"])
    #comments = models.Comment(content=request.form["contents"])
    return redirect(url_for('gamescmt'))



@login_required
@app.route('/sportscmt', methods=["GET", "POST"])
def sportscmt():
    if request.method == "GET":
        sportscmtd = models.Sportscmtd.select().limit(100)
        return render_template("sportscmt.html",sportscmtd=sportscmtd)
    models.Sportscmtd.create(user=g.user._get_current_object(), content=request.form["contents"])
    #comments = models.Comment(content=request.form["contents"])
    return redirect(url_for('sportscmt'))


@login_required
@app.route('/bussnescmt', methods=["GET", "POST"])
def bussnescmt():
    if request.method == "GET":
        bussnescmtd = models.Bussnescmtd.select().limit(100)
        return render_template("bussnescmt.html",bussnescmtd=bussnescmtd)
    models.Bussnescmtd.create(user=g.user._get_current_object(), content=request.form["contents"])
    #comments = models.Comment(content=request.form["contents"])
    return redirect(url_for('bussnescmt'))


@login_required
@app.route('/politcscmt', methods=["GET", "POST"])
def politcscmt():
    if request.method == "GET":
        politcscmtd = models.Politcscmtd.select().limit(100)
        return render_template("politcscmt.html",politcscmtd=politcscmtd)
    models.Politcscmtd.create(user=g.user._get_current_object(), content=request.form["contents"])
    #comments = models.Comment(content=request.form["contents"])
    return redirect(url_for('politcscmt'))





#deleting comments
@app.route('/delete_comment/<int:comment_id>')
@login_required
def delete_comment(comment_id):
    try:
        my_comment = models.Comment.select().where(models.Comment.id == comment_id).get()
        time_comment = models.Comment.select().where((models.Comment.timestamp) <
                                          (datetime.date.today() - datetime.timedelta(days=2)))
    except models.Comment.DoesNotExist:
        abort(404)
    my_comment.delete_instance()
    #post.execute()
    flash("This comment has successfully been deleted.", "success")
    return redirect(url_for('educationcmt',my_comment=my_comment,time_comment=time_comment))



@app.route('/delete_gamescmt/<int:comment_id>')
@login_required
def delete_gamescmt(comment_id):
    try:
        my_gamescmt = models.Gamescmtd.select().where(models.Gamescmtd.id == comment_id).get()
        time_comment = models.Comment.select().where((models.Comment.timestamp) <
                                          (datetime.date.today() - datetime.timedelta(days=2)))
    except models.Gamescmtd.DoesNotExist:
        abort(404)
    my_gamescmt.delete_instance()
    #post.execute()
    flash("This comment has successfully been deleted.", "success")
    return redirect(url_for('gamescmt',my_gamescmt=my_gamescmt))



@app.route('/delete_sportscmt/<int:comment_id>')
@login_required
def delete_sportscmt(comment_id):
    try:
        my_sportscmt = models.Sportscmtd.select().where(models.Sportscmtd.id == comment_id).get()
        time_comment = models.Comment.select().where((models.Comment.timestamp) <
                                          (datetime.date.today() - datetime.timedelta(days=2)))
    except models.Sportscmtd.DoesNotExist:
        abort(404)
    my_sportscmt.delete_instance()
    #post.execute()
    flash("This comment has successfully been deleted.", "success")
    return redirect(url_for('sportscmt',my_sportscmt=my_sportscmt))





@app.route('/delete_bussnescmt/<int:comment_id>')
@login_required
def delete_bussnescmt(comment_id):
    try:
        my_bussnescmt = models.Bussnescmtd.select().where(models.Bussnescmtd.id == comment_id).get()
        time_comment = models.Comment.select().where((models.Comment.timestamp) <
                                          (datetime.date.today() - datetime.timedelta(days=2)))
    except models.Bussnescmtd.DoesNotExist:
        abort(404)
    my_bussnescmt.delete_instance()
    #post.execute()
    flash("This comment has successfully been deleted.", "success")
    return redirect(url_for('bussnescmt',my_bussnescmt=my_bussnescmt))





@app.route('/delete_politcscmt/<int:comment_id>')
@login_required
def delete_politcscmt(comment_id):
    try:
        my_politcscmt = models.Politcscmtd.select().where(models.Politcscmtd.id == comment_id).get()
        time_comment = models.Comment.select().where((models.Comment.timestamp) <
                                          (datetime.date.today() - datetime.timedelta(days=2)))
    except models.Politcscmtd.DoesNotExist:
        abort(404)
    my_politcscmt.delete_instance()
    #post.execute()
    flash("This comment has successfully been deleted.", "success")
    return redirect(url_for('politcscmt',my_politcscmt=my_politcscmt))







#deleting myalbum images
@app.route('/delete_myalbum/<int:image_id>')
@login_required
def delete_myalbum(image_id):
    try:
        my_album = models.Images.select().where(models.Images.id == image_id).get()

    except models.Images.DoesNotExist:
        abort(404)
    my_album.delete_instance()
    #post.execute()
    flash("This image has successfully been deleted.", "success")
    return redirect(url_for('my_album',my_album=my_album))



#deleting drphoto
@app.route('/delete_drphoto/<int:drphoto_id>')
@login_required
def delete_drphoto(drphoto_id):
    try:
        my_drphoto = models.Drphoto.select().where(models.Drphoto.id == drphoto_id).get()
    except models.Drphoto.DoesNotExist:
        abort(404)
    my_drphoto.delete_instance()
    flash("This photo has successfully been deleted.", "success")
    return redirect(url_for('results',my_drphoto=my_drphoto))




#deleting drphoto
@app.route('/delete_gamesimage/<int:gamesimage_id>')
@login_required
def delete_gamesimage(gamesimage_id):
    try:
        my_gamesimage = models.Gamesimage.select().where(models.Gamesimage.id == gamesimage_id).get()
    except models.Gamesimage.DoesNotExist:
        abort(404)
    my_gamesimage.delete_instance()
    flash("This photo has successfully been deleted.", "success")
    return redirect(url_for('ourgames',my_gamesimage=my_gamesimage))




#delete all photoes
@app.route('/delete_gamesimages')
@login_required
def delete_gamesimages():
    try:
        my_gamesphotos = models.Gamesimage.delete()
    except models.Gamesimages.DoesNotExist:
        abort(404)
    my_gamesphotos.execute()
    flash("This photos has successfully been deleted.", "success")
    return redirect(url_for('ourgames',my_gamesphotos=my_gamesphotos))


@app.route('/delete_sportsimage')
@login_required
def delete_sportsimage():
    try:
        my_sportsphotos = models.Sportsimage.delete()
    except models.Sportsimages.DoesNotExist:
        abort(404)
    my_sportsphotos.execute()
    flash("This photos has successfully been deleted.", "success")
    return redirect(url_for('oursports',my_sportsphotos=my_sportsphotos))



@app.route('/delete_bussnesimage')
@login_required
def delete_bussnesimage():
    try:
        my_bussnesphotos = models.Bussnesimage.delete()
    except models.Bussnesimages.DoesNotExist:
        abort(404)
    my_bussnesphotos.execute()
    flash("This photos has successfully been deleted.", "success")
    return redirect(url_for('ourbussnes',my_bussnesphotos=my_bussnesphotos))



@app.route('/delete_politcsimage')
@login_required
def delete_politcsimage():
    try:
        my_politcsphotos = models.Politcsimages.delete()
    except models.Politcsimages.DoesNotExist:
        abort(404)
    my_politcsphotos.execute()
    flash("This photos has successfully been deleted.", "success")
    return redirect(url_for('ourpolitcs',my_politcsphotos=my_politcsphotos))





@app.route('/delete_drphotos')
@login_required
def delete_drphotos():
    try:
        my_drphotos = models.Drphoto.delete()
    except models.Drphoto.DoesNotExist:
        abort(404)
    my_drphotos.execute()
    flash("This photos has successfully been deleted.", "success")
    return redirect(url_for('results',my_drphotos=my_drphotos))







#deleting photomessage
@app.route('/delete_photomsg/<int:photosmsg_id>')
@login_required
def delete_photomsg(photosmsg_id):
    try:
        my_photomsg = models.Photomessage.select().where(models.Photomessage.id == photosmsg_id).get()
    except models.Photomessage.DoesNotExist:
        abort(404)
    my_photomsg.delete_instance()
    flash("This discription has successfully been deleted.", "success")
    return redirect(url_for('results',my_photomsg=my_photomsg))




#deleting photomessage
@app.route('/delete_gamesimagemsg/<int:photosmsg_id>')
@login_required
def delete_gamesimagemsg(photosmsg_id):
    try:
        my_gamesimagemsg = models.Gamesmsg.select().where(models.Gamesmsg.id == photosmsg_id).get()
    except models.Gamesmsg.DoesNotExist:
        abort(404)
    my_gamesimagemsg.delete_instance()
    flash("This discription has successfully been deleted.", "success")
    return redirect(url_for('ourgames',my_gamesimagemsg=my_gamesimagemsg))




#deleting photomessage
@app.route('/delete_sportsimagemsg/<int:photosmsg_id>')
@login_required
def delete_sportsimagemsg(photosmsg_id):
    try:
        my_sportsimagemsg = models.Sportsmsg.select().where(models.Sportsmsg.id == photosmsg_id).get()
    except models.Sportsmsg.DoesNotExist:
        abort(404)
    my_sportsimagemsg.delete_instance()
    flash("This discription has successfully been deleted.", "success")
    return redirect(url_for('oursports',my_sportsimagemsg=my_sportsimagemsg))




#deleting photomessage
@app.route('/delete_bussnesimagemsg/<int:photosmsg_id>')
@login_required
def delete_bussnesimagemsg(photosmsg_id):
    try:
        my_bussnesimagemsg = models.Bussnesmsg.select().where(models.Bussnesmsg.id == photosmsg_id).get()
    except models.Bussnesmsg.DoesNotExist:
        abort(404)
    my_bussnesimagemsg.delete_instance()
    flash("This discription has successfully been deleted.", "success")
    return redirect(url_for('ourbussnes',my_bussnesimagemsg=my_bussnesimagemsg))



#deleting photomessage
@app.route('/delete_politcsimagemsg/<int:photosmsg_id>')
@login_required
def delete_politcsimagemsg(photosmsg_id):
    try:
        my_politcsimagemsg = models.Politcsmsg.select().where(models.Politcsmsg.id == photosmsg_id).get()
    except models.Politcsmsg.DoesNotExist:
        abort(404)
    my_politcsimagemsg.delete_instance()
    flash("This discription has successfully been deleted.", "success")
    return redirect(url_for('ourpolitcs',my_politcsimagemsg=my_politcsimagemsg))


@login_required
@app.route('/videochat')
def videochat():
    return render_template('chat.html')





@app.route('/mysearch', methods=['GET', 'POST'])
def mysearch():
    search = forms.MusicSearchForm(request.form)
    if request.method == 'POST':
        mysearch = (models.User.select(models.User.username)
        .join(models.FTSsearch, on=(models.User.id == models.FTSsearch.docid))
        .where(models.FTSsearch.match(search))
        .dicts())
        return mysearch
    return render_template('index.html', form=search, mysearch=mysearch)





if __name__ == '__main__':
    models.initialize()
    try:
        with models.DATABASE.transaction():
            models.User.create_user(
                username ='luckius',
                email ='luckiusevodius@gmail.com',
                password ='pass',
                admin = True,
            )
    except ValueError:
        pass
    app.run(debug = DEBUG, host = HOST, port = PORT)
    #socketio.run(app, debug=DEBUG, host=HOST, port=PORT)
    #app.run(debug=True)
