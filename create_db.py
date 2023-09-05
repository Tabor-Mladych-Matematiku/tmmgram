from db_model import Location
from tmmgram import db, app

with app.app_context():
    db.create_all()

    if db.session.query(Location).first() is None:  # no locations in the database
        default_location = Location("Kdekoli", 1)
        db.session.add(default_location)
        db.session.commit()
