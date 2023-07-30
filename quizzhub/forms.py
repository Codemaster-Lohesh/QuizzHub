from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField,  BooleanField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from quizzhub.models import User

class RegistrationForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email= StringField('Email',validators=[DataRequired(), Email()])
    password= PasswordField('Password',validators=[DataRequired()])
    confirm_password= PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit= SubmitField('Sign Up')

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different username')
        
    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different email')

class LoginForm(FlaskForm):
    email= StringField('Email',validators=[DataRequired(), Email()])
    password= PasswordField('Password',validators=[DataRequired()])
    remember= BooleanField('Remember me')
    submit= SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
    email= StringField('Email',validators=[DataRequired(), Email()])
    picture= FileField('Profile picture',validators=[FileAllowed(['jpg','png'])])
    submit= SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username:
            user=User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different username')
        
    def validate_email(self,email):
        if email.data != current_user.email:
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different email')
            

class CreateQuizForm(FlaskForm):
    quiz_name = StringField('Quiz Name')
    question = StringField('Question',validators=[DataRequired()])
    option1= StringField('Option 1',validators=[DataRequired()])
    option2= StringField('Option 2',validators=[DataRequired()])
    option3= StringField('Option 3',validators=[DataRequired()])
    option4= StringField('Option 4',validators=[DataRequired()])
    correct_option= RadioField('Correct option', choices=[
        ('option1', 'Option 1'),
        ('option2', 'Option 2'),
        ('option3', 'Option 3'),
        ('option4', 'Option 4')
    ])
    submit = SubmitField('Create Quiz')

class AttemptQuiz(FlaskForm):
    answer= RadioField('Choose your answer',choices=[
        ('option1', 'Option 1'),
        ('option2', 'Option 2'),
        ('option3', 'Option 3'),
        ('option4', 'Option 4')
    ])
    submit = SubmitField('Submit Answer')

class SearchForm(FlaskForm):
    user=StringField('User Search',validators=[DataRequired()])
    submit = SubmitField('Search')