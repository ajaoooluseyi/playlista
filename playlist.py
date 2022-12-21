from flask import Flask, render_template, url_for, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///playlist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    songtitle = db.Column(db.String(200), unique=True, nullable=False )
    artiste = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, songtitle=" ", artiste=" ", rating=" "):
        self.songtitle = songtitle
        self.artiste = artiste
        self.rating = rating


@app.route("/", methods=["POST", "GET"])
def welcome():
    if request.method == 'POST':
        title = request.form["title"]

        artiste = request.form["artiste"]

        rating = request.form["rating"]

        entry = playlist(songtitle=title,artiste=artiste,rating=rating)

        try:
            db.session.add(entry)
            db.session.commit()
            return redirect('/table')
        except:
            return 'You might have added this song before. Please add a new track or try again'
    else:
        return render_template ('welcome.html')



@app.route("/table", methods=["POST", "GET"])
def table():
    tracks = playlist.query.order_by(date_created).all()
    return render_template("table.html",  tracks=tracks)




@app.route("/delete/<int:id>")
def delete(id):
    track_delete = playlist.query.get_or_404(id)

    try:
        db.session.delete(track_delete)
        db.session.commit()
        return redirect("/table")
    except:
        return "There was a problem deleting the task. Try Again!"


@app.route("/update/<int:id>", methods = ['POST', 'GET'])
def update(id):
    track = playlist.query.get_or_404(id)

    if request.method =='POST':
        if track:
            db.session.delete(track)
            db.session.commit()


        songtitle = request.form["tent"]

        artiste = request.form["tiste"]

        rating = request.form["ting"]

        track=playlist(songtitle=songtitle,artiste=artiste,rating=rating)


        try:
            db.session.add(track)
            db.session.commit()
            return redirect('/table')
        except:
            return "Track not updated. Try Again!"

    else:
        return render_template('update.html', track=track)

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
