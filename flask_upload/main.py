from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
import os
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired


app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretkey"
app.config["UPLOAD_FOLDER"]= "static/files"


class UploadFile(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route("/", methods= ["GET", "POST"])
@app.route("/home", methods= ["GET", "POST"])
def home():
    form = UploadFile()
    if form.validate_on_submit():
        uploaded_file = form.file.data
        uploaded_file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"], secure_filename(file.filename)))
        return "File has being uploaded"
    return render_template("index.html", form=form)



if __name__ == "__main__":
    app.run(debug=True)
