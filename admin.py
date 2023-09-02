from flask import Blueprint

from helpers import render, admin_required

admin_blueprint = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


@admin_blueprint.route('/admin')
@admin_required
def admin():
    return render("admin.html")


from admin_users import users_blueprint
admin_blueprint.register_blueprint(users_blueprint)
from admin_locations import locations_blueprint
admin_blueprint.register_blueprint(locations_blueprint)
from admin_post_rating import rating_blueprint
admin_blueprint.register_blueprint(rating_blueprint)
