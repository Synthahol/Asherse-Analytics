import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email

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

mail = Mail(app)
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

        msg = Message(subject=subject, recipients=[app.config["MAIL_USERNAME"]])
        msg.body = f"From: {first_name} {last_name} <{email}>\n\n{message}"

        try:
            mail.send(msg)
            flash("Email sent successfully", "success")
        except Exception as e:
            app.logger.error(f"Error sending email: {e}")
            flash(f"An error occurred: {str(e)}", "danger")

        return redirect("/")

    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
