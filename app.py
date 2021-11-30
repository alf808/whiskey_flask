#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from sqlalchemy import func
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# FINISHED: connect to a local postgresql database, SEE: config.py
# FINISHED: flask db init, flask db migrate, flask db upgrade
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

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # FINISHED: replace with real venues data.
  # FINISHED: num_upcoming_shows based on number of upcoming shows per venue.
    data = []
    content = Venue.query.distinct(Venue.city, Venue.state).all()
    if content:
        for area in content:
            area_obj = {
                'city': area.city,
                'state': area.state,
                'venues': []
            }
            # get all the venues specific to city, state
            venue_locs = Venue.query.filter(Venue.state == area.state).filter(Venue.city == area.city).all()
            for venue in venue_locs:
                venue_obj = {
                    'id': venue.id,
                    'name': venue.name,
                    # upcoming shows filtered by current venue and shows later than now
                    'num_upcoming_shows': len(db.session.query(Shows).filter(Shows.c.venue_id == venue.id, Shows.c.start_time > datetime.now()).all())
                }
                area_obj['venues'].append(venue_obj)
                
            data.append(area_obj)
            
    return render_template('pages/venues.html', areas=data)    

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # FINISHED: implement search on venues with partial string search.
  # Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get('search_term', '')
    data = Venue.query.filter(Venue.name.ilike(f"%{search_term}%")).all()
    response = {'count': len(data), 'data': data}

    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # FINISHED: replace with real venue data from the venues table, using venue_id
    venue = Venue.query.get(venue_id)
    now = datetime.now()
    events = db.session.query(Shows).filter(Shows.c.venue_id==venue_id).all()
    data = {
        'id': venue.id,
        'name': venue.name,
        'genres': venue.genres,
        'address': venue.address,
        'city': venue.city,
        'state': venue.state,
        'phone': venue.phone,
        'website': venue.website,
        'facebook_link': venue.facebook_link,
        'seeking_talent': venue.seeking_talent,
        'seeking_description': venue.seeking_description,
        'image_link': venue.image_link,
        'upcoming_shows': [],
        'upcoming_shows_count': 0,
        'past_shows': [],
        'past_shows_count': 0
    }
    for event in events:
        artist = Artist.query.get(event.artist_id)
        show_obj = {
            'artist_id': artist.id,
            'artist_name': artist.name,
            'artist_image_link': artist.image_link,
            'start_time': str(event.start_time)
        }
        if event.start_time > now:
            data['upcoming_shows'].append(show_obj)
        else:
            data['past_shows'].append(show_obj)
        data['upcoming_shows_count'] = len(data['upcoming_shows'])
        data['past_shows_count'] = len(data['past_shows'])
        
    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # FINISHED: insert form data as a new Venue record in the db, instead
  # FINISHED: modify data to be the data object returned from db insertion
    req = request.form
    vform = VenueForm(req)
    seeking_talent = False
    if req['seeking_description']:
        seeking_talent = True
    venue_obj = {
        'name': req['name'],
        'city': req['city'],
        'state': req['state'],
        'address': req['address'],
        'phone': req['phone'],
        'genres': req.getlist('genres'),
        'facebook_link': req['facebook_link'],
        'image_link': req['image_link'],
        'website': req['website_link'],
        'seeking_talent': seeking_talent,
        'seeking_description': req['seeking_description'],
    }
    venue = Venue(**venue_obj)

    try:
        db.session.add(venue)
        db.session.commit()
        # on successful db insert, flash success
        flash(f'Venue {req["name"]} was successfully listed!')
    except Exception as e:
        # TODO: on unsuccessful db insert, flash an error instead.
        flash(f'An error occurred. Venue {req["name"]} could not be listed. {e}')
        db.session.rollback()
        db.session.flush()
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['POST', 'DELETE'])
def delete_venue(venue_id):
  # FINISHED: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    try:
        venue = Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
        flash(f'The venue and its associated events were successfully deleted.')
    except Exception as e:
        flash(f'An error occurred. Venue {req["name"]} could not be deleted. {e}')
        db.session.rollback()
        db.session.flush()
    finally:
        db.session.close()

    # FINISHED: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # FINISHED: replace with real data returned from querying the database
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
  # FINISHED: implement search on artists with partial string search.
  # Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
    search_term = request.form.get('search_term', '')
    data = Artist.query.filter(Artist.name.ilike(f"%{search_term}%")).all()
    response = {'count': len(data), 'data': data}
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))    
    

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # FINISHED: replace with real artist data from the artist table, using artist_id
    artist = Artist.query.get(artist_id)
    now = datetime.now()
    gigs = db.session.query(Shows).filter(Shows.c.artist_id==artist_id).all()
    data = {
        'id': artist.id,
        'name': artist.name,
        'genres': artist.genres,
        'city': artist.city,
        'state': artist.state,
        'phone': artist.phone,
        'website': artist.website,
        'facebook_link': artist.facebook_link,
        'seeking_venue': artist.seeking_venue,
        'seeking_description': artist.seeking_description,
        'image_link': artist.image_link,
        'upcoming_shows': [],
        'upcoming_shows_count': 0,
        'past_shows': [],
        'past_shows_count': 0
    }
    for gig in gigs:
        venue = Venue.query.get(gig.venue_id)
        show_obj = {
            'venue_id': venue.id,
            'venue_name': venue.name,
            'venue_image_link': venue.image_link,
            'start_time': str(gig.start_time)
        }
        if gig.start_time > now:
            data['upcoming_shows'].append(show_obj)
        else:
            data['past_shows'].append(show_obj)
        data['upcoming_shows_count'] = len(data['upcoming_shows'])
        data['past_shows_count'] = len(data['past_shows'])
        
    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    seeking_venue = False
    if artist.seeking_venue:
        seeking_venue = True
    artist_obj = {
        'name': artist.name,
        'genres': artist.genres,
        'city': artist.city,
        'state': artist.state,
        'phone': artist.phone,
        'image_link': artist.image_link,
        'website_link': artist.website,
        'facebook_link': artist.facebook_link,
        'seeking_venue': seeking_venue,
        'seeking_description': artist.seeking_description
    }
    form.process(**artist_obj)
    # FINISHED: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # FINISHED: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
    req = request.form
    form = ArtistForm(req)
    try:
        artist = Artist.query.get(artist_id)
        seeking_venue = False
        if req['seeking_venue']:
            seeking_venue = True
        artist.name = req.get('name')
        artist.genres = req.getlist('genres')
        artist.city = req.get('city')
        artist.state = req.get('state')
        artist.phone = req.get('phone')
        artist.image_link = req.get('image_link')
        artist.website = req.get('website_link')
        artist.facebook_link = req.get('facebook_link')
        artist.seeking_venue = seeking_venue
        artist.seeking_description = req.get('seeking_description')
        db.session.commit()
        flash(f'Artist {artist.name} or {req["name"]} successfully updated')
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        flash(f'Something went wrong. {e}')
    finally:
        db.session.close()
        
    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    seeking_talent = False
    if venue.seeking_talent:
        seeking_talent = True
    venue_obj = {
        'name': venue.name,
        'genres': venue.genres,
        'address': venue.address,
        'city': venue.city,
        'state': venue.state,
        'phone': venue.phone,
        'image_link': venue.image_link,
        'website_link': venue.website,
        'facebook_link': venue.facebook_link,
        'seeking_talent': seeking_talent,
        'seeking_description': venue.seeking_description
    }
    form.process(**venue_obj)
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
    req = request.form
    form = VenueForm(req)
    try:
        venue = Venue.query.get(venue_id)
        seeking_venue = False
        if req['seeking_talent']:
            seeking_venue = True
        venue.name = req.get('name')
        venue.genres = req.getlist('genres')
        venue.address = req.get('address')
        venue.city = req.get('city')
        venue.state = req.get('state')
        venue.phone = req.get('phone')
        venue.image_link = req.get('image_link')
        venue.website = req.get('website_link')
        venue.facebook_link = req.get('facebook_link')
        venue.seeking_venue = seeking_venue
        venue.seeking_description = req.get('seeking_description')
        db.session.commit()
        flash(f'Venue {venue.name} or {req["name"]} successfully updated')
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        flash(f'Something went wrong. {e}')
    finally:
        db.session.close()    
        return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # FINISHED: replace with real venues data.
    # db.Table Shows has no query method. Had to use db.session
    # content = db.session.query(Shows).join(Artist).all()
    content = db.session.query(Shows).order_by(Shows.c.start_time.desc()).all()
    data = []
    for event in content:
        artist = Artist.query.get(event.artist_id)
        venue = Venue.query.get(event.venue_id)
        data.append({
            'venue_id': event.venue_id,
            'venue_name': venue.name,
            'artist_id': event.artist_id,
            'artist_name': artist.name,
            'artist_image_link': artist.image_link,
            'start_time': str(event.start_time)
        })
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # FINISHED: insert form data as a new Show record in the db, instead
    req = request.form
    show_obj = {
        'artist_id': req['artist_id'],
        'venue_id': req['venue_id'],
        'start_time': req['start_time']
    }
    show = Shows.insert().values(**show_obj)
    try:
        db.session.execute(show)
        db.session.commit()
        # on successful db insert, flash success
        flash('Show was successfully listed!')
    except Exception as e:
        # TODO: on unsuccessful db insert, flash an error instead.
        flash(f'An error occurred. Show could not be listed. {e}')
        db.session.rollback()
        db.session.flush()
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
