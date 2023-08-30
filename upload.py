import os

from flask import redirect, request, flash, Blueprint, url_for, send_from_directory
from flask_login import login_required
from werkzeug.utils import secure_filename

from config import config
from helpers import render

upload_blueprint = Blueprint('upload', __name__, template_folder='templates', static_folder='static')

allowed_extensions = ", .".join(config['allowed_extensions'])


def allowed_file(filename: str):
    print(filename)
    return '.' in filename and \
       filename.rsplit('.', 1)[1].lower() in config['allowed_extensions']


@upload_blueprint.route('/upload', methods=("GET", "POST"))
@login_required
def upload():
    if request.method == "POST":

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('Musíte vybrat soubor!', 'danger')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            flash('Musíte vybrat soubor!', 'danger')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(config['upload_folder'], filename))
            flash(f"Soubor byl úspěšně nahrán.", "success")
            return redirect(url_for('upload.download_file', name=filename))
        else:
            flash(f"Soubor není podporován, povolené přípony jsou: {allowed_extensions}.", "danger")
            return redirect(request.url)

    return render("upload.html", title="Nahrát soubor", allowed_extensions=allowed_extensions)


@upload_blueprint.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(config["upload_folder"], name)
