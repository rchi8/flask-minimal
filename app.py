from email_validator import validate_email, EmailNotValidError
from flask import Flask, current_app, g, render_template, request, url_for, redirect, flash, make_response, session
import logging 
import os
from flask_mail import Mail, Message
# from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)

app.config["SECRET_KEY"] = "hfskjshsis3heA"
app.config["DEBUG_TB_TNTERCEPT_REDIRECTS"] = False
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

mail = Mail(app)

app.logger.setLevel(logging.DEBUG)
app.logger.critical("fatal eroor")
app.logger.error("error")
app.logger.warning("warning")
app.logger.info("info")
app.logger.debug("debug")

@app.route("/")
def index():
    return redirect(url_for("contact"))

@app.route("/contact/")
def contact():
    response = make_response(render_template("contact.html"))

    response.set_cookie("flaskbook key", "flask value")

    session["username"] = "ichiro"


    return response



@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        is_valid = True

        if not username:
            flash("no username")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))

        # メールを送る
        send_email(
            email,
            "問い合わせありがとうございました",
            "contact_mail",
            username=username,
            description=description,
        )

        return render_template("contact_mail.html", username=username, description=description)

    
    

def send_email(to, subject, template, **kwargs):
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)

