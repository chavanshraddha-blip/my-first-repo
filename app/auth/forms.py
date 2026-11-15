import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional, Regexp
from flask_login import current_user
from app.models.user import User


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(message='Username is required.'),
            Length(min=3, max=30, message='Username must be between 3 and 30 characters.'),
            Regexp('^[a-zA-Z0-9_]+$', message='Username can only contain letters, numbers, and underscores.')
        ]
    )
    email = StringField(
        'Email Address',
        validators=[
            DataRequired(message='Email address is required.'),
            Email(message='Please provide a valid email address.')
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message='Password is required.'),
            Length(min=6, message='Password must be at least 6 characters long.')
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(message='Please confirm your password.'),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    submit = SubmitField('Create Account')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data.strip()).first()
        if user:
            raise ValidationError('This username is already taken. Please choose another.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.strip().lower()).first()
        if user:
            raise ValidationError('An account with this email already exists.')


class LoginForm(FlaskForm):
    login_id = StringField(
        'Username or Email',
        validators=[DataRequired(message='Please enter your username or email.')]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(message='Please enter your password.')]
    )
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class EditProfileForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(message='Username is required.'),
            Length(min=3, max=30, message='Username must be between 3 and 30 characters.'),
            Regexp('^[a-zA-Z0-9_]+$', message='Username can only contain letters, numbers, and underscores.')
        ]
    )
    bio = TextAreaField(
        'Bio / About Me',
        validators=[Optional(), Length(max=500, message='Bio cannot exceed 500 characters.')]
    )
    current_password = PasswordField('Current Password (only if changing password)')
    new_password = PasswordField(
        'New Password',
        validators=[Optional(), Length(min=6, message='New password must be at least 6 characters.')]
    )
    confirm_new_password = PasswordField(
        'Confirm New Password',
        validators=[EqualTo('new_password', message='Passwords must match.')]
    )
    submit = SubmitField('Save Profile')

    def validate_username(self, username):
        if username.data.strip() != current_user.username:
            user = User.query.filter_by(username=username.data.strip()).first()
            if user:
                raise ValidationError('This username is already taken.')
