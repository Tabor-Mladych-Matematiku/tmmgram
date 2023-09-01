import base64
import os
import uuid

from flask import redirect, request, flash, Blueprint, send_from_directory
from flask_login import login_required, current_user

from config import config
from db_model import Post, db
from helpers import render

upload_blueprint = Blueprint('upload', __name__, template_folder='templates', static_folder='static')


@upload_blueprint.route('/upload', methods=("GET", "POST"))
@login_required
def upload():
    if request.method == "POST":
        # check if the file was uploaded
        if 'file' not in request.form or request.form['file'] == '':
            flash('Musíte vybrat soubor!', 'danger')
            return redirect(request.url)
        file = request.form['file']

        if file[:23] != "data:image/jpeg;base64,":
            flash('Vybraný soubor není podporován.', 'danger')
            return redirect(request.url)
        file = file[23:]

        # save the uploaded file
        filename = f"{current_user.id_user}_{uuid.uuid4()}.jpg"
        file_path = os.path.join(config['upload_folder'], filename)
        with open(file_path, "wb") as image_file:
            image_file.write(base64.decodebytes(file.encode()))

        # create a post in database
        post = Post(file_path, current_user.id_user)
        db.session.add(post)
        db.session.commit()

        flash(f"Soubor byl úspěšně nahrán.", "success")
        return redirect("/")

    return render("upload.html", title="Nahrát soubor", allowed_files=config['allowed_files'])


@upload_blueprint.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(config["upload_folder"], name)
