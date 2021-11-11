from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField,PasswordField,SubmitField,BooleanField, TextAreaField,SelectField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from app.models import Categories, Users

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

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('password',validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


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
    title = StringField('Title', validators=[DataRequired()])
    category = SelectField(u'Category', choices=[], validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class PreviewForm(FlaskForm):
    cover_picture = FileField('Cover image', validators=[FileAllowed(['jpg','png','jpeg'])])
    pic_desc = StringField('Cover image description', validators=[DataRequired()])
    submit = SubmitField('Upload')

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

class ContactForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')

class CommentsForm(FlaskForm):
    comments = TextAreaField('Comments', validators=[DataRequired()])
    submit = SubmitField('Send')

class SendNotificationsForm(FlaskForm):
    email = StringField('Recipient email', validators=[DataRequired(),Email()])
    notification = TextAreaField('Notification message', validators=[DataRequired()])
    submit = SubmitField('Send')

    def validate_email(self,email):
        user = Users.query.filter_by(email = email.data).first()
        if user is None:
            raise ValidationError('Email does not exist!')

class ContactInfoForm(FlaskForm):
    company_name = StringField('Company name')
    address = StringField('Address')
    phone = StringField('Phone number')
    email = StringField('Email address', validators=[Email()])
    city = StringField('City')

class SocialMediaAccountsForm(FlaskForm):
    facebook = StringField('Facebook accoun link')
    instagram = StringField('Instagram account link')
    youtube = StringField('Youtube account link')
    twitter = StringField('Twitter account link')
    
