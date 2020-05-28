from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy

from forms import RegistrationForm, LoginForm, CommunicationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Communication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auto_type = db.Column(db.String(120))
    select_type = db.Column(db.Integer())
    receiver = db.Column(db.String(50), nullable=False)


    def __repr__(self):
        return f"Comunication('{self.auto_type}')"



posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home",  methods=['GET', 'POST'])
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/communication")
def com():
    return render_template('communication.html', title='communication')

@app.route("/auto_message", methods=['GET', 'POST'])
def auto_message():
    form = CommunicationForm()
    if form.validate_on_submit():
     #check_message
        if form.select_type.data == 1 :
            x = 'δεν εχω ρεύμα'
        elif form.select_type.data == 2 :
            x = 'Δεν εχω νερό'
        elif form.select_type.data == 3 :
            x = 'Δεν εχω internet'
        elif form.select_type.data == 4 :
            x = 'Δεν εχω ζεστό νετό'
        else :
            x ='Δεν έχω θέρμανση'
        com = Communication(auto_type=x, receiver= form.receiver.data)
        db.session.add(com)
        db.session.commit()
        print(com.auto_type)
        flash('Το μήνυμα εστάλει στο χρήστη !', 'success')
        return redirect(url_for('home'))
    return render_template('auto_message.html', title='auto_message', form=form)

@app.route("/write_message")
def write_message():
    form = CommunicationForm()
    return render_template('write_message.html', title='auto_message', form=form)



@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():

        user = User(username=form.username.data, email=form.email.data, password= form.password.data )
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
