import secrets
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from wtforms import Form, StringField, SubmitField
from wtforms.validators import DataRequired

# Initialize Flask app
app = Flask(__name__)

# Automatically generate a secure secret key
app.config['SECRET_KEY'] = secrets.token_hex(16)  # Generate a 32-character hex string

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Simple form class
class MyForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Route for home page with form submission
@app.route("/", methods=["GET", "POST"])
def home():
    form = MyForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        flash(f"Form submitted successfully with name: {name}", "success")
        return redirect(url_for("home"))
    return render_template("home.html", form=form)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
