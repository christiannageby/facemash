#!flask/bin/python
from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import random
import os
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
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
    index = random.sample(range(1, len(Persons.query.all())), 2)
    return render_template('index.html', contestants = [Persons.query.filter_by(id=index[0]).first_or_404(),Persons.query.filter_by(id=index[1]).first_or_404()])

@app.route('/upload')
def upload() -> render_template:
    return render_template('upload.html')

@app.route('/vote/<int:winner>/<int:loser>')
def vote(winner: int, loser: int) -> redirect:
    winner = Persons.query.filter_by(id=winner).first()
    loser = Persons.query.filter_by(id=loser).first()

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
    if request.method == 'POST':
        # if file is missing flash message
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            location = os.path.join("static/images/", filename)
            file.save(location)

            person = Persons(path=location)
            db.session.add(person)
            db.session.commit()
            return redirect(url_for('home', name=filename))

if __name__ == '__main__':
    app.run(port=8888, host='127.0.0.1')
