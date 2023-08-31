import os
import uuid

from flask import redirect, request, flash, Blueprint, url_for, send_from_directory
from flask_login import login_required, current_user

from config import config
from db_model import Post, db
from helpers import render

upload_blueprint = Blueprint('upload', __name__, template_folder='templates', static_folder='static')

allowed_extensions = ", ".join(f".{ext}" for ext in config['allowed_extensions'])


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
        if not file or file.filename == '':
            flash('Musíte vybrat soubor!', 'danger')
            return redirect(request.url)

        # check the extension
        if '.' not in file.filename:
            extension = ""
        else:
            extension = file.filename.rsplit('.', 1)[1].lower()
        if extension not in config['allowed_extensions']:
            flash(f"Soubor s příponou '{extension}' není podporován, povolené přípony jsou: {allowed_extensions}.", "danger")
            return redirect(request.url)

        # save the uploaded file
        filename = f"{current_user.id_user}_{uuid.uuid4()}.{extension}"
        file_path = os.path.join(config['upload_folder'], filename)
        file.save(file_path)

        # create a post in database
        post = Post(file_path, current_user.id_user)
        db.session.add(post)
        db.session.commit()

        flash(f"Soubor byl úspěšně nahrán.", "success")
        return redirect("/")

    return render("upload.html", title="Nahrát soubor", allowed_extensions=allowed_extensions)


@upload_blueprint.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(config["upload_folder"], name)
