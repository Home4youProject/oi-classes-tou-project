import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from Home4u import app, db, bcrypt
from Home4u.forms import RegistrationForm, LoginForm, UpdateAccountForm, ReviewForm, AddHouseForm, UpdateHouseForm, HouseSelectForm, SearchForm, ResultsForm
from Home4u.models import User, House, HouseSelector, SearchInfo, Review, stayed
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime


@app.route("/")
@app.route("/home",methods=['GET', 'POST'])
def home():
    logo_image = url_for('static', filename='logo.png')
    return render_template('home.html', image_file=logo_image)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/search", methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        search = SearchInfo(location=form.location.data, arrival_date=form.arrival_date.data, guests=form.guests.data)
        db.session.add(search)
        db.session.commit()
        return redirect(url_for('search_results'))
    return render_template('search.html', title='Search', form=form)

@app.route("/search_results", methods=['GET', 'POST'])
def search_results():
    form = SearchForm()
    searched_houses = House.query.filter_by(city=form.location.data).all()
    if form.validate_on_submit():
        select = HouseSelector(house_id=form.house_id.data)
        db.session.add(select)
        db.session.commit()
        flash('Your house has been succesfully saved!', 'success')
        return redirect(url_for('home'))
    return render_template('search_results.html', query=House.query.filter_by(city='patra').all(), title='Search Results', form=form)


@app.route("/report")
def report():
    return render_template('report.html', title='Report')

@app.route("/user_review_list")
def user_review_list():
    form = ReviewForm()
    homes = House.query.filter_by(id=current_user.id).all()
    if form.validate_on_submit():
        return redirect(url_for('user_review'))
    return render_template('user_review_list.html', title='Houses List', form=form)

@app.route("/user_review")
def user_review():
    form = ReviewForm()
    
    if form.validate_on_submit():
        review = Review(reviewer=current_user.id, recipient=homes.id, stars=form.stars.data, comments=form.comments.data)
        db.session.add(review)
        db.session.commit()
        flash('Your review has been succesfully saved!', 'success')
        return redirect(url_for('home'))
    return render_template('user_review.html', title='Add a Review', form=form)

@app.route("/owner_review")
def owner_review():
    return render_template('owner_review.html', title='Add a Review')

@app.route("/communication")
def communication():
    return render_template('communication.html', title='Communication')

@app.route("/write_message")
def write_message():
    return render_template('write_message.html', title='Communication')

@app.route("/auto_message")
def auto_message():
    return render_template('auto_message.html', title='Communication')

@app.route("/register_house", methods=['GET', 'POST'])
def register_house():
    form = AddHouseForm()
    if form.validate_on_submit():
        house = House(house_name=form.house_name.data, city=form.city.data, postal_code=form.postal_code.data, address=form.address.data, square_meters=form.square_meters.data, price=form.price.data, house_type=form.house_type.data, visitors=form.visitors.data, user_id=current_user.id)
        db.session.add(house)
        db.session.commit()
        flash('Your house has been succesfully saved!', 'success')
        return redirect(url_for('login'))
    return render_template('register_house.html', title='Add House', form=form)




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

def save_picture2(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/house_pics', picture_fn)

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

@app.route("/edit_house", methods=['GET', 'POST'])
@login_required
def edit_house():
    form = UpdateHouseForm()
   
    house = House.query.filter_by(id=current_user.selected_id).first()
    if form.validate_on_submit():
        
        if form.picture.data:
            picture_file = save_picture2(form.picture.data)
            house.image_file = picture_file
        house.house_name = form.house_name.data
        house.city = form.city.data
        house.postal_code = form.postal_code.data
        house.address = form.address.data
        house.square_meters = form.square_meters.data
        house.price = form.price.data
        house.house_type = form.house_type.data
        house.visitors = form.visitors.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
       
        form.house_name.data = house.house_name
        form.city.data = house.city
        form.postal_code.data = house.postal_code
        form.address.data = house.address
        form.square_meters.data = house.square_meters
        form.price.data = house.price
        form.house_type.data = house.house_type
        form.visitors.data = house.visitors
    image_file = url_for('static', filename='house_pics/' + house.image_file)
    return render_template('edit_house.html', title='Edit House',
                           image_file=image_file, form=form, house=house)





@app.route("/house_list", methods=['GET', 'POST'])
def house_list():
    form = HouseSelectForm()
    houses = House.query.filter_by(user_id=current_user.id).all()
    
    if form.validate_on_submit():
        current_user.selected_id=form.house_id.data
        db.session.commit()
        return redirect(url_for('edit_house'))
    return render_template('house_list.html', query=House.query.filter_by(user_id=current_user.id).all() , title='Houses', form=form)



@app.route("/payment", methods=['GET', 'POST'])
def payment():
    form = PaymentForm()
    houses = House.query.filter_by(user_id=current_user.id).all()
    
    if form.validate_on_submit():
        current_user.selected_id=form.house_id.data
        db.session.commit()
        return redirect(url_for('edit_house'))
    return render_template('payment.html', query=House.query.filter_by(user_id=current_user.id).all() , title='Houses', form=form)