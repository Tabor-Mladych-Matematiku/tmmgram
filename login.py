from flask import redirect, request, flash, render_template, Blueprint
from flask_bcrypt import check_password_hash
from flask_login import current_user, login_user, login_required, logout_user

from config import config
from db_model import Admin, User
from helpers import is_safe_url

login_blueprint = Blueprint('login', __name__, template_folder='templates', static_folder='static')


@login_blueprint.route('/login', methods=("GET", "POST"))
def login():
    if current_user.is_authenticated:
        return redirect('/')

    username = ""
    if request.method == "POST":
        username = request.form["user"].strip()
        password = request.form["password"]

        if username == "admin" and password == config['admin_password']:
            login_user(Admin(), remember=True)
            next_url = request.args.get('next')
            if next_url and is_safe_url(next_url):
                return redirect(next_url)
            return redirect('/')
        else:
            user: User = User.query.filter_by(name=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                next_url = request.args.get('next')
                if next_url and is_safe_url(next_url):
                    return redirect(next_url)
                return redirect('/')
            else:
                flash(f"Neplatné přilašovací údaje.", "danger")

    return render_template("login.html", title="Přihlášení", username=username)


@login_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login')
