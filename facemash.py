#!flask/bin/python
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import configparser
import random
import os

app = Flask(__name__)
app.config.from_pyfile('config.py.sample')
db = SQLAlchemy(app)

class Persons(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(), unique=True, nullable=False)
    upvotes = db.Column(db.Integer(), nullable=False, default=0)
    downvotes = db.Column(db.Integer(), nullable=False, default=0)
    elo_rank = db.Column(db.Integer(), nullable=False, default=1200)

    def __init__(self, path: str):
        self.upvotes = 0
        self.downvotes = 0
        self.elo_rank = 1200
        self.path = path

    def __repr__(self):
        return '<Person %r>' % self.id
K = 32

@app.route('/')
def home() -> render_template:
    """ Try to serve the main view if it fails due to ValueError catch it and serve a Too few contestants page instead
        Else show a generic error template with the exception printed out."""
    try:
        return render_template('index.html', contestants = random.sample(Persons.query.all(), 2))
    except ValueError:
        return render_template('error.html', exception="Too few contestants in database to bee able to start the game.")
    except Exception as excp:
        return render_template('error.html', exception=excp)

@app.route('/upload')
def upload() -> render_template:
    """ Serve the upload page statically, this should not be able to fail. No try/catch needed for now."""
    return render_template('upload.html')

@app.route('/vote/<int:winner>/<int:loser>')
def vote(winner: int, loser: int) -> redirect:
    """ The function for the vote, modify the users elo_rank by the correct formulas.
        :returns a redirect"""
    # Fetch the winner and the looser from the database from the database by ID.
    winner: Persons = Persons.query.filter_by(id=winner).first()
    loser: Persons = Persons.query.filter_by(id=loser).first()
    
    winner.upvotes += 1
    loser.downvotes += 1

    ea = 1 / (1 + 10 ** ((loser.elo_rank - winner.elo_rank) / 400))
    eb = 1 / (1 + 10 ** ((winner.elo_rank - loser.elo_rank) / 400))

    winner.elo_rank = winner.elo_rank + (K * (1 - ea))
    loser.elo_rank = loser.elo_rank + (K * (0 - eb))

    db.session.commit()
    return redirect(url_for('home'))

@app.route('/upload_image', methods=['GET', 'POST'])
def upload_file() -> redirect:
    """Upload files to static/images and return a redirect """
    if request.method == 'POST':
        # if there is no file in the request throw an error
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            return redirect(request.url)
        # If a file is sent convert it to a secure filename
        # TODO: Set it as a UUID16 or something
        if file:
            filename = secure_filename(file.filename)
            # TODO: Remove hard coded path
            location = os.path.join(app.config['IMAGE_DIR'], filename)
            file.save(location)

            # Insert the image in the database.
            person = Persons(path=location)
            db.session.add(person)
            db.session.commit()

            return redirect(url_for('home', name=filename))

if __name__ == '__main__':
    app.run(port=8888, host='127.0.0.1')
