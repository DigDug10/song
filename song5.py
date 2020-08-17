from datetime import datetime

from flask import Flask, session, render_template, flash, request, redirect, url_for
from forms1 import LoginForm, RegistrationForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = '1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db4.sqlite3'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(40), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    songs = db.relationship('Song', backref='user', lazy=True)

    def __repr__(self):
        return '<User  {}>'.format(self.user)


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat = db.Column(db.String(30))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    numb = db.Column(db.Integer)
    artist = db.Column(db.String(40))
    title = db.Column(db.String(40))
    date_created = db.Column(db.DateTime, default=datetime.now)


cat = "Song"


@app.route('/user/<user>')
def index(user):
    user = User(user=user, password_hash='1234')
    db.session.add(user)
    db.session.commit()

    print(f'Added User!')
    return '<h1> Added User!</h1>'


@app.route('/<cat>/<numb>/<artist>/<title>')
def index1(cat, numb, artist, title):
    song = Song(cat=cat, user_id=2, numb=numb, artist=artist, title=title)
    db.session.add(song)
    db.session.commit()

    print(f'Added Song!')
    return '<h1> Added Song!</h1>'


@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' in session:
        print(session['username'])
        q = db.session.query(Song, User).filter(User.id == Song.user_id)
        print(q)
        return render_template('main5v1.html', title='Songs I\'m ', songs=q)
    else:
        return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
@app.route('/user_home', methods=['GET', 'POST'])
def user_home():
    if 'username' in session:
        print(cat)
        print(session)
        print(session['username'])
        name = (session['username'])
        u = User.query.filter_by(user=name).first()
        q = Song.query.filter(Song.user_id == u.id, Song.cat == cat).order_by(Song.artist)
        print(q)
        print(u)
        print(u.id, u.user)
        return render_template('main5_2.html', title=name + ' Songs', songs=q, user=name)
    else:
        return redirect(url_for('login'))

@app.route('/user_home/<cat>', methods=['GET', 'POST'])
def user_home_cat(cat):
    if 'username' in session:
        cat = cat
        print(cat)
        print(session)
        print(session['username'])
        name = (session['username'])
        u = User.query.filter_by(user=name).first()
        q = Song.query.filter(Song.user_id == u.id, Song.cat == cat).order_by(Song.artist)
        print(q)
        print(u)
        print(u.id, u.user)
        return render_template('main5_2.html', title=name + ' Songs', songs=q, user=name)
    else:
        return redirect(url_for('login'))


@app.route('/user')
def user():
    users = User.query.all()

    return render_template('user1.html', users=users)


@app.route('/<path:text>')
def misc(text):
    # name = name
    songs = Song.query.all()

    return render_template('main5v1.html', songs=songs)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if 'username' in session:
        print('yes in session')
        print(form.username.data)
        form.username.data = session['username']
    if form.validate_on_submit():
        session['username'] = form.username.data
        return redirect(url_for('user_home'))
    print(form.validate_on_submit())
    print("Try again")
    flash('Great')
    return render_template('login1.html', title='Login', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    users = User()
    form = RegistrationForm()
    if request.method == "POST":
        if form.validate_on_submit():
            users.user = form.username.data
            session['username'] = form.username.data
            users.password_hash = form.password.data
            db.session.add(users)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            print("Try again")
            return render_template('signup1.html', title='Register ---', form=form)
    else:
        print("Not yet")
        return render_template('signup1.html', title='Register ---', form=form)


@app.route('/insert', methods=['GET', 'POST'])
def insert():
    print("Insert")
    print(request.method)
    if request.method == 'POST':
        print(request.form['cat'])
        cat = request.form['cat']
        name = (session['username'])
        u = User.query.filter_by(user=name).first()
        user_id = u.id
        numb = request.form['numb']
        artist = request.form['artist']
        title = request.form['title']
        songs = Song(cat=cat, user_id=user_id, numb=numb, artist=artist, title=title)
        db.session.add(songs)
        db.session.commit()

        flash("Song Added")

        return redirect(url_for('home'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Song.query.get(request.form.get('id'))
        my_data.cat = request.form['cat']
        my_data.numb = request.form['numb']
        my_data.artist = request.form['artist']
        my_data.title = request.form['title']
        print('My below')
        print(my_data)
        db.session.commit()

        flash("Song was Updated ")

        return redirect(url_for('home'))


@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    my_data = Song.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    flash("Song is Gone!!")

    return redirect(url_for('home'))


print("Hello")

if __name__ == '__main__':
    app.run(debug=True)
