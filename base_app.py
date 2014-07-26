from flask import Flask, session, render_template, redirect, request, flash
from werkzeug.utils import secure_filename
import lookup
import os



app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
# app.jinja_env.undefined = jinja2.StrictUndefined

app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route("/")
def index():
    return render_template("receiveaudio.html")

@app.route("/music_recognition", methods=['POST'])   
def music_recognition():
	file = request.files['user_audio']
	filename = secure_filename("user_input.wav")
	file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	return str(lookup.lookup(filename))

@app.route("/success")
def successful_ident():
	return render_template("generateresults.html")



if __name__ == "__main__":
    app.run(debug=True)