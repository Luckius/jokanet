from flask_wtf import Form
from wtforms import StringField, PasswordField,TextAreaField,SubmitField, SelectField
from wtforms.validators import (DataRequired, Regexp, ValidationError,Email,
                                Length, EqualTo,)
from flask_wtf.file import FileField, FileAllowed
from models import User





def name_exists(form, field):
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('user with that name aready exist.')


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('user with this email aready exist.')


class RegisterForm(Form):
    username = StringField(
        'Username',
        validators = [
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message = ("username should be one word, letters,"
                           "numbers and underscores only.")
            ),
            name_exists
        ])
    email = StringField(
        'Email',
        validators = [
            DataRequired(),
            Email(),
            email_exists

        ])
    password = PasswordField(
        'Password',
        validators = [
            DataRequired(),
            Length(min=2),
            EqualTo('password2',message = 'password must match')

        ])
    password2 = PasswordField(
        'Confirm Password',
        validators = [DataRequired()]
    )





'''class UpdateAccountForm(Form):
    username = StringField(
        'Username',
        validators = [
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message = ("username should be one word, letters,"
                           "numbers and underscores only.")
            ),
            name_exists
        ])
    email = StringField(
        'Email',
        validators = [
            DataRequired(),
            Email(),
            email_exists

        ])
    password = PasswordField(
        'Password',
        validators = [
            DataRequired(),
            Length(min=2),
            EqualTo('password2',message = 'password must match')

        ])
    password2 = PasswordField(
        'Confirm Password',
        validators = [DataRequired()]
    )
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')'''


class PhotoForm(Form):
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')




class LoginForm(Form):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('password', validators = [DataRequired()])


#render_kw={"rows": 10, "cols": 11},
class PostForm(Form):
    content = TextAreaField("Whats up?", validators = [DataRequired()])



class PhotomessageForm(Form):
    content = TextAreaField("add message?", validators = [DataRequired()])



class GamesmsgForm(Form):
    content = TextAreaField("add message?", validators = [DataRequired()])



class SportsmsgForm(Form):
    content = TextAreaField("add message?", validators = [DataRequired()])


class BussnesmsgForm(Form):
    content = TextAreaField("add message?", validators = [DataRequired()])


class PolitcsmsgForm(Form):
    content = TextAreaField("add message?", validators = [DataRequired()])



class MessageForm(Form):
    content = TextAreaField("message?", validators=[DataRequired()])

class CommentForm(Form):
    content = TextAreaField("comment?", validators=[DataRequired()])


class MusicSearchForm(Form):
    select = SelectField()
    search = StringField('')
