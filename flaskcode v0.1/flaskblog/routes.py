import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime


posts = [
    {
        'author': 'Xristos Mpouras',
        'title': 'Athens Sunny Appartment',
        'content': '4 beds',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Nikos Papanikolaou',
        'title': 'Great View Loft in Thiseio',
        'content': '2 beds',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    logo_image = url_for('static', filename='logo.png')
    return render_template('home.html', posts=posts, image_file=logo_image)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/search")
def search():
    return render_template('search.html', title='Search')

@app.route("/report")
def report():
    return render_template('report.html', title='Report')

@app.route("/user_review")
def user_review():
    return render_template('user_review.html', title='User Review')

@app.route("/communication")
def communication():
    return render_template('communication.html', title='Communication')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, phone=form.phone.data, firstname=form.firstname.data, surname=form.surname.data, sex=form.sex.data, birth_date=form.birth_date.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        current_user.birth_date = form.birth_date.data
        current_user.firstname = form.firstname.data
        current_user.surname = form.surname.data
        current_user.sex = form.sex.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.birth_date.data = current_user.birth_date
        form.firstname.data = current_user.firstname
        form.surname.data = current_user.surname
        form.sex.data = current_user.sex
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

