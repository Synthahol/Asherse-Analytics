import logging
import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email

from extensions import mail

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder="Assets", template_folder="templates")
app.secret_key = os.getenv("SECRET_KEY", "your_default_secret_key")

# Configure Flask-Mail
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

mail.init_app(app)
csrf = CSRFProtect(app)


# Flask-WTF Form
class ContactForm(FlaskForm):
    first_name = StringField("", validators=[DataRequired()])
    last_name = StringField("", validators=[DataRequired()])
    email = StringField("", validators=[DataRequired(), Email()])
    subject = StringField("", validators=[DataRequired()])
    message = TextAreaField("", validators=[DataRequired()])
    submit = SubmitField("Send Message")


@app.route("/", methods=["GET", "POST"])
def home():
    form = ContactForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data

        from email_utils import (
            send_email,  # Move the import here to avoid circular import
        )

        body = f"From: {first_name} {last_name} <{email}>\n\n{message}"
        success, msg = send_email(subject, [app.config["MAIL_USERNAME"]], body)
        if success:
            flash(msg, "success")
            logging.info(f"Email sent successfully to {email}")
        else:
            flash(f"An error occurred: {msg}", "danger")
            logging.error(f"Failed to send email to {email}: {msg}")

        return redirect("/")

    return render_template("index.html", form=form)


if __name__ == "__main__":
    logging.info("Starting the Flask application...")
    app.run(debug=True)
