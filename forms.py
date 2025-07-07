from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.widgets import TextArea
from typing import Optional
import re

class CKTextAreaWidget(TextArea):
    """Custom textarea widget for CKEditor"""
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    """Custom textarea field for CKEditor"""
    widget = CKTextAreaWidget()

class CustomValidator:
    """Custom validation methods"""
    
    @staticmethod
    def validate_username(form, field):
        """Validate username format"""
        username = field.data
        if not re.match("^[a-zA-Z0-9_]+$", username):
            raise ValidationError('Username can only contain letters, numbers, and underscores.')
    
    @staticmethod
    def validate_password_strength(form, field):
        """Validate password strength"""
        password = field.data
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        if not re.search(r"[A-Z]", password):
            raise ValidationError('Password must contain at least one uppercase letter.')
        if not re.search(r"[a-z]", password):
            raise ValidationError('Password must contain at least one lowercase letter.')
        if not re.search(r"\d", password):
            raise ValidationError('Password must contain at least one number.')

class RegisterForm(FlaskForm):
    """User registration form"""
    name = StringField(
        "Full Name",
        validators=[
            DataRequired(message="Full name is required"),
            Length(min=2, max=100, message="Name must be between 2 and 100 characters")
        ],
        render_kw={"placeholder": "Enter your full name", "class": "form-control"}
    )
    
    username = StringField(
        "Username",
        validators=[
            DataRequired(message="Username is required"),
            Length(min=3, max=20, message="Username must be between 3 and 20 characters"),
            CustomValidator.validate_username
        ],
        render_kw={"placeholder": "Choose a username", "class": "form-control"}
    )
    
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Email is required"),
            Email(message="Please enter a valid email address"),
            Length(max=120, message="Email must be less than 120 characters")
        ],
        render_kw={"placeholder": "Enter your email", "class": "form-control"}
    )
    
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password is required"),
            CustomValidator.validate_password_strength
        ],
        render_kw={"placeholder": "Create a strong password", "class": "form-control"}
    )
    
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(message="Please confirm your password"),
            EqualTo('password', message='Passwords must match')
        ],
        render_kw={"placeholder": "Confirm your password", "class": "form-control"}
    )

class LoginForm(FlaskForm):
    """User login form"""
    username = StringField(
        "Username",
        validators=[
            DataRequired(message="Username is required"),
            Length(min=3, max=20, message="Username must be between 3 and 20 characters")
        ],
        render_kw={"placeholder": "Enter your username", "class": "form-control"}
    )
    
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password is required")
        ],
        render_kw={"placeholder": "Enter your password", "class": "form-control"}
    )

class ArticleForm(FlaskForm):
    """Article creation/editing form"""
    title = StringField(
        "Title",
        validators=[
            DataRequired(message="Title is required"),
            Length(min=5, max=200, message="Title must be between 5 and 200 characters")
        ],
        render_kw={"placeholder": "Enter article title", "class": "form-control"}
    )
    
    content = CKTextAreaField(
        "Content",
        validators=[
            DataRequired(message="Content is required"),
            Length(min=50, message="Content must be at least 50 characters long")
        ],
        render_kw={"placeholder": "Write your article content here", "rows": "10"}
    )
    
    keywords = StringField(
        "Keywords",
        validators=[
            DataRequired(message="Keywords are required"),
            Length(min=3, max=200, message="Keywords must be between 3 and 200 characters")
        ],
        render_kw={"placeholder": "Enter keywords separated by commas", "class": "form-control"}
    )

class ContactForm(FlaskForm):
    """Contact form"""
    name = StringField(
        "First Name",
        validators=[
            DataRequired(message="First name is required"),
            Length(min=2, max=50, message="Name must be between 2 and 50 characters")
        ],
        render_kw={"placeholder": "Enter your first name", "class": "form-control"}
    )
    
    surname = StringField(
        "Last Name",
        validators=[
            DataRequired(message="Last name is required"),
            Length(min=2, max=50, message="Last name must be between 2 and 50 characters")
        ],
        render_kw={"placeholder": "Enter your last name", "class": "form-control"}
    )
    
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Email is required"),
            Email(message="Please enter a valid email address"),
            Length(max=120, message="Email must be less than 120 characters")
        ],
        render_kw={"placeholder": "Enter your email", "class": "form-control"}
    )
    
    message = TextAreaField(
        "Message",
        validators=[
            DataRequired(message="Message is required"),
            Length(min=10, max=1000, message="Message must be between 10 and 1000 characters")
        ],
        render_kw={"placeholder": "Write your message here", "class": "form-control", "rows": "5"}
    )

class PredictionForm(FlaskForm):
    """Form for machine learning predictions"""
    days = SelectField(
        "Prediction Days",
        choices=[
            (7, "7 Days"),
            (14, "14 Days"),
            (30, "30 Days")
        ],
        coerce=int,
        default=7,
        validators=[DataRequired(message="Please select prediction period")],
        render_kw={"class": "form-control"}
    )