from flask import request, redirect, flash, Blueprint

from db_model import db, Location
from helpers import render, admin_required

locations_blueprint = Blueprint('locations', __name__, template_folder='templates', static_folder='static')


def get_all_locations():
    return Location.query.order_by(Location.id_location).all()


@locations_blueprint.route('/admin/locations')
@admin_required
def locations_list():
    locations = get_all_locations()
    return render("locations_list.html", locations=locations)


@locations_blueprint.route('/admin/locations/new', methods=("GET", "POST"))
@admin_required
def locations_new():
    if request.method == "POST":
        location = Location(request.form["name"], float(request.form["followers_coefficient"]))
        db.session.add(location)
        db.session.commit()
        return redirect("/admin/locations")
    return render("location_edit.html")


@locations_blueprint.route('/admin/locations/<id_location>', methods=("GET", "POST"))
@admin_required
def locations_edit(id_location):
    location: Location = Location.query.get(id_location)
    if location is None:
        flash(f"Stanoviště s id_location={id_location} neexistuje.", "warning")
        return redirect("/admin/locations")

    if request.method == "POST":
        location.name = request.form["name"]
        location.followers_coefficient = float(request.form["followers_coefficient"])
        db.session.add(location)
        db.session.commit()
        return redirect("/admin/locations")
    else:
        return render("location_edit.html", location=location)


@locations_blueprint.route('/admin/locations/<id_location>/delete', methods=("POST",))
@admin_required
def locations_delete(id_location):
    location = Location.query.get(id_location)
    if location is None:
        flash(f"Stanoviště s id_location={id_location} neexistuje.", "warning")
        return redirect("/admin/locations")

    db.session.delete(location)
    db.session.commit()
    flash(f'Stanoviště "{location.name}" (id={location.id}) smazáno.', "success")
    return redirect("/admin/locations")
