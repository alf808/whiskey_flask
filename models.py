from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
# association table for many-many relationship between venues and artists
Shows = db.Table(
    'shows',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('artist_id', db.ForeignKey('artists.id'), nullable=False),
    db.Column('venue_id', db.ForeignKey('venues.id'), nullable=False),
    db.Column('start_time', db.DateTime, nullable=False)
)

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(200))
    shows = db.relationship('Venue', secondary=Shows, backref='venue', cascade='all, delete')

    # FINISHED: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(200))
    gigs = db.relationship('Artist', secondary=Shows, backref='artist', cascade='all, delete')


    # FINISHED: implement any missing fields, as a database migration using Flask-Migrate

# FINISHED: Implement Show and Artist models, See model relationships above.
