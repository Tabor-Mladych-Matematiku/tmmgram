from flask import request, redirect, flash, Blueprint

from db_model import User, db
from helpers import render, admin_required

users_blueprint = Blueprint('users', __name__, template_folder='templates', static_folder='static')


@users_blueprint.route('/admin/users')
@admin_required
def users_list():
    users = User.query.order_by(User.name).all()
    return render("users.html", users=users)


@users_blueprint.route('/admin/users/new', methods=("GET", "POST"))
@admin_required
def users_new():
    if request.method == "POST":
        user = User(request.form["name"], request.form["password"], request.form["note"])
        db.session.add(user)
        db.session.commit()
        return redirect("/admin/users")
    return render("user_edit.html")


@users_blueprint.route('/admin/users/<id_user>', methods=("GET", "POST"))
@admin_required
def users_edit(id_user):
    user: User = User.query.get(id_user)
    if user is None:
        flash(f"Uživatel s id_user={id_user} neexistuje.", "warning")
        return redirect("/admin/users")

    if request.method == "POST":
        user.name = request.form["name"]
        if request.form["password"]:
            user.set_password(request.form["password"])
        user.note = request.form["note"]
        db.session.add(user)
        db.session.commit()
        return redirect("/admin/users")
    else:
        return render("user_edit.html", user=user)


@users_blueprint.route('/admin/users/<id_user>/delete', methods=("POST",))
@admin_required
def users_delete(id_user):
    user = User.query.get(id_user)
    if user is None:
        flash(f"Uživatel s id_user={id_user} neexistuje.", "warning")
        return redirect("/admin/users")

    db.session.delete(user)
    db.session.commit()
    flash(f'Uživatel "{user.name}" (id={user.id}) smazán.', "success")
    return redirect("/admin/users")
