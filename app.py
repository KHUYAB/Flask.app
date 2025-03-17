from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
app.config['SECRET_KEY'] = '188a4ba320e79190bdf7'  # Required for CSRF protection

# Flask-Login Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirect to login page if not authenticated

# Dummy User Class
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Dummy User Database
users = {'admin': {'password': 'password'}}

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Login Form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Contact Form
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')

# Email Configuration
EMAIL_ADDRESS = "your-email@gmail.com"
EMAIL_PASSWORD = "your-app-password"

@app.route('/')
@login_required  # Requires login to access
def home():
    return render_template('index.html')

@app.route('/about')
@login_required  # Requires login to access
def about():
    return render_template('about.html')

@app.route('/skills')
@login_required  # Requires login to access
def skills():
    return render_template('skills.html')


@app.route('/projects')
@login_required  # Requires login to access
def projects():
    return render_template('projects.html')

@app.route('/contact', methods=['GET', 'POST'])
@login_required  # Requires login to access
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data
        
        # Compose email
        msg = EmailMessage()
        msg.set_content(f"Name: {name}\nEmail: {email}\nMessage: {message}")
        msg["Subject"] = "New Contact Form Submission"
        msg["From"] = email
        msg["norhankuyab@gmail.com"] = EMAIL_ADDRESS

        # Send email
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)
            flash("Message sent successfully!", "success")
        except Exception as e:
            flash(f"Error sending message: {str(e)}", "danger")

        return redirect(url_for('contact'))
    
    return render_template('contact.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Run the Flask Application
if __name__ == '__main__':
    app.run(debug=True)
