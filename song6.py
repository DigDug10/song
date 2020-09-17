from datetime import datetime, date

from flask import Flask, session, render_template, flash, request, redirect, url_for, jsonify, make_response
from forms1 import LoginForm, RegistrationForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = '1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db6.sqlite3'

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
    cat = db.Column(db.String(15))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    numb = db.Column(db.Integer)
    artist = db.Column(db.String(40))
    title = db.Column(db.String(40))
    date_created = db.Column(db.DateTime, default=datetime.now)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cat = db.Column(db.String(15))
    cat_text = db.Column(db.String(30))


class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    friend_name = db.Column(db.String(40))
    user_request = db.Column(db.Date, default=date.today)
    acceptance = db.Column(db.Date)


cat = "Songs"


# ---------- Manual add of data code:


@app.route('/user/<user>')
def index(user):
    user = User(user=user, password_hash='1234')
    db.session.add(user)
    db.session.commit()

    print(f'Added User!')
    return '<h1> Added User!</h1>'


@app.route('/<cat>/<numb>/<artist>/<title>')
def index1(cat, numb, artist, title):
    song = Song(cat=cat, user_id=1, numb=numb, artist=artist, title=title)
    db.session.add(song)
    db.session.commit()

    print(f'Added Song!')
    return '<h1> Added Song!</h1>'


@app.route('/cat/<category>/<description>')
def index2(category, description):
    cat_add = Category(cat=category, cat_text=description)
    db.session.add(cat_add)
    db.session.commit()

    print(f'Added Category!')
    return '<h1> Added Category!</h1>'


@app.route('/friends/<id>/<friend_id>')
def index3(id, friend_id):
    friend_info = User.query.filter_by(id=friend_id).first()
    print(id)
    print(friend_id)
    print(friend_info.user)
    friend = Friends(user_id=id, friend_id=friend_id, friend_name=friend_info.user)
    db.session.add(friend)
    db.session.commit()

    print(f'Added Friend!')
    return '<h1> Added Friend!</h1>'


# ---------  Song displays code:


@app.route('/', methods=['GET', 'POST'])
def user_home():
    if 'username' in session:
        if 'cat' in session:
            print(cat)
            print("In session")
        else:
            cat = 'Songs'
            print("Not in session")
        print(cat)
        print("This is user_home")
        category = Category.query.all()
        print(category)
        print(session)
        print(session['username'])
        name = (session['username'])
        u = User.query.filter_by(user=name).first()
        q = Song.query.filter(Song.user_id == u.id, Song.cat == cat).order_by(Song.numb)
        print(q)
        print(u)
        print(u.id, u.user)
        return render_template('main6_2.html', title=name + ' Songs', songs=q, user=name, cat=cat, category=category)
    else:
        return redirect(url_for('login'))


@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' in session:
        print(session['username'])
        print('Home')
        q = db.session.query(Song, User).filter(User.id == Song.user_id).order_by(User.id, Song.cat, Song.numb)
        print(q)
        return render_template('main6.html', title='Songs I\'m ', songs=q)
    else:
        return redirect(url_for('login'))


@app.route('/test', methods=['GET', 'POST'])
def test():
    if 'username' in session:
        print('Test area')
        print(session)
        name = (session['username'])
        print(name)
        cat = 'Songs'
        u = User.query.filter_by(user=name).first()
        print(u.id)
        my_friends = Friends.query.filter_by(user_id=u.id).all()
        print(my_friends, my_friends[0].friend_id)
        category = Category.query.all()
        # q = Song.query.filter(Song.user_id == 1, Song.cat == cat).order_by(Song.numb)
        q = db.session.query(Song, my_friends).filter_by(user_id=my_friends.friend_id).order_by(my_friends.friend_id, Song.cat, Song.numb)
        print(q)
        # return render_template('main6_2.html', title=name + ' Songs', songs=q, user=name, cat=cat, category=category)
        return render_template('main6_1.html', title='Songs I\'m ', songs=q)
    else:
        return redirect(url_for('login'))


@app.route('/user_home/<cat>', methods=['GET', 'POST'])
def user_home_cat(cat):
    if 'username' in session:
        cat = cat
        print(cat)
        print("This is user_home_cat")
        category = Category.query.all()
        print(category)
        print(session)
        print(session['username'])
        name = (session['username'])
        u = User.query.filter_by(user=name).first()
        q = Song.query.filter(Song.user_id == u.id, Song.cat == cat).order_by(Song.numb)
        print(q)
        print(u)
        print(u.id, u.user)
        return render_template('main6_2.html', title=name + ' Songs', songs=q, user=name, cat=cat, category=category)
    else:
        return redirect(url_for('login'))


@app.route("/json", methods=["POST"])
def json():
    if request.is_json:
        req = request.get_json()
        print(req)
    print(request)

    return "Thanks", 200


# --------------  Friends code:


@app.route('/friend', methods=['GET', 'POST'])
def friend():
    if 'username' in session:
        print("This is friend home")
        print(session['username'])
        name = (session['username'])
        u = User.query.filter_by(user=name).first()
        friend = Friends.query.filter_by(user_id=u.id).order_by(Friends.friend_id)
        print(friend)
        print(u)
        print(u.id, u.user)
        print(cat)
        return render_template('friends6.html', title=name + ' Friends', user=u, friend=friend)
    else:
        return redirect(url_for('login'))


@app.route('/insert_friend', methods=['GET', 'POST'])
def insert_friend():
    print("Insert friend")
    name = (session['username'])
    u = User.query.filter_by(user=name).first()
    friend_id = request.form['friend_id']
    friend_info = User.query.filter_by(id=friend_id).first()
    print(friend_id)
    print(friend_info.user)
    friend = Friends(user_id=u.id, friend_id=friend_id, friend_name=friend_info.user)
    db.session.add(friend)
    db.session.commit()

    print(f'Added Friend!')
    flash("Friend is requested!")
    return redirect(url_for('friend', title=' Friends', user=user, friend=friend))


@app.route('/delete_friend/<id>', methods=['GET', 'POST'])
def delete_friend(id):
    print("Delete friend")
    my_data = Friends.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    print(f'Friend Deleted!')
    flash("Friend is deleted!")

    return redirect(url_for('friend', title=' Friends', user=user, friend=friend))


@app.route('/accept_friend/<id>', methods=['GET', 'POST'])
def accept_friend(id):
    print("Accepted friend")
    my_data = Friends.query.get(id)
    my_data.acceptance = date.today()
    print(my_data.acceptance)
    db.session.commit()

    print(f'Friend Accepted!')
    flash("Friend is accepted!")

    return redirect(url_for('friend', title=' Friends', user=user, friend=friend))


# --------------Login, register, user and song displays


@app.route('/user')
def user():
    users = User.query.all()

    return render_template('user1.html', users=users)


@app.route('/<path:text>')
def misc(text):
    # name = name
    songs = Song.query.all()

    return render_template('main6_2.html', songs=songs)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print(cat)
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


# -----------Code for Song mods -------


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

        return redirect(url_for('user_home_cat', cat=cat))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Song.query.get(request.form.get('id'))
        my_data.cat = request.form['cat']
        cat = my_data.cat
        my_data.numb = request.form['numb']
        my_data.artist = request.form['artist']
        my_data.title = request.form['title']
        print(cat)
        print('My below')
        print(my_data)
        db.session.commit()

        flash("Song was Updated ")

        return redirect(url_for('user_home_cat', cat=cat))


@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    my_data = Song.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    flash("Song is Gone!!")

    return redirect(url_for('user_home_cat', cat=cat))


print("Hello")

if __name__ == '__main__':
    app.run(debug=True)
