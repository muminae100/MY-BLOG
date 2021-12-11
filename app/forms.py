from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField,PasswordField,SubmitField,BooleanField, TextAreaField,SelectField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from app.models import Categories, Subscribers, Users, Tags

class RegistrationForm(FlaskForm):
    username = StringField('Username',
    validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
    validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = Users.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('That username is taken!')

    def validate_email(self,email):
        user = Users.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('That email is taken!')



class AuthorRegistrationForm(FlaskForm):
    bio = StringField('Bio',
    validators=[DataRequired(),Length(min=20,max=500)])
    address = StringField('Address')
    phone = StringField('Phone number')
    city = StringField('City')
    facebook = StringField('Your facebook page link')
    instagram = StringField('Your instagram account link')
    twitter = StringField('Your twitter account link')
    youtube = StringField('Your youtube channel link')
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = Users.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('That username is taken!')

    def validate_email(self,email):
        user = Users.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('That email is taken!')



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('password',validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')



class AuthorUpdateAccountForm(FlaskForm):
    username = StringField('Username',
    validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    bio = StringField('Bio',
    validators=[DataRequired(),Length(min=20,max=500)])
    address = StringField('Address')
    phone = StringField('Phone number')
    email = StringField('Email address', validators=[Email()])
    city = StringField('City')
    facebook = StringField('Facebook accoun link')
    instagram = StringField('Instagram account link')
    youtube = StringField('Youtube account link')
    twitter = StringField('Twitter account link')
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username:
            user = Users.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('That username is taken!')

    def validate_email(self,email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('That email is taken!')



class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
    validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg','png','jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username:
            user = Users.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('That username is taken!')

    def validate_email(self,email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('That email is taken!')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(),Length(min=5,max=150)])
    category = SelectField(u'Category', choices=[], validators=[DataRequired()])
    cover_picture = StringField('Cover image link', validators=[DataRequired()])
    pic_desc = StringField('Cover image description', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

class VideoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(),Length(min=25,max=100)])
    category = SelectField(u'Category', choices=[], validators=[DataRequired()])
    video_url = StringField('Youtube video id (e.g Us1Gh_1j3zb)', validators=[DataRequired()])
    video_desc = StringField('Video description', validators=[DataRequired()])
    submit = SubmitField('Post')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self,email):
        user = Users.query.filter_by(email = email.data).first()
        if user is None:
            raise ValidationError('Email does not exist!')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
    validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class SubscribeForm(FlaskForm):
    email = StringField('Your Email', validators=[DataRequired(),Email()])
    submit = SubmitField('Subscribe')

    def validate_email(self,email):
        user = Subscribers.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('That email is already subscribed to our newsletters!')


class ContactForm(FlaskForm):
    email = StringField('Your email', validators=[DataRequired(),Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')

class CommentsForm(FlaskForm):
    comments = StringField('Comments', validators=[DataRequired()])
    submit = SubmitField('Post comment')

class SendNotificationsForm(FlaskForm):
    email = StringField('Recipient email', validators=[DataRequired(),Email()])
    notification = TextAreaField('Notification message', validators=[DataRequired()])
    submit = SubmitField('Send')

    def validate_email(self,email):
        user = Users.query.filter_by(email = email.data).first()
        if user is None:
            raise ValidationError('Email does not exist!')

    
