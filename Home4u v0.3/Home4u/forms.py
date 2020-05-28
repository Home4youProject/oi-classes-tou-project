from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from Home4u.models import User, House, HouseSelector, SearchInfo , Review, stayed
from wtforms.fields.html5 import DateField


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Κωδικός', validators=[DataRequired()])
    confirm_password = PasswordField('Επαλήθευση Κωδικού',
                                     validators=[DataRequired(), EqualTo('password')])
    phone = IntegerField('Τηλέφωνο')
    birth_date = DateField('Ημερομηνία Γέννησης', format='%Y-%m-%d')
    firstname = StringField('Όνομα')
    surname = StringField('Επίθετο')
    sex = StringField('Φύλο')
    submit = SubmitField('Εγγραφή')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Κωδικός', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Σύνδεση')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Ενημέρωση Εικόνας Προφίλ', validators=[FileAllowed(['jpg', 'png'])])
    phone = IntegerField('Τηλέφωνο')
    birth_date = DateField('Ημερομηνία Γέννησης', format='%Y-%m-%d')
    firstname = StringField('Όνομα')
    surname = StringField('Επίθετο')
    sex = StringField('Φύλο')
    submit = SubmitField('Ενημέρωση')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class ReviewForm(FlaskForm):
    reviewer = IntegerField('Reviewer')
    recipient = IntegerField('Id')
    stars = IntegerField('Stars')
    comments = StringField('Comments')
    submit = SubmitField('Προσθήκη Αξιολόγησης')
    submit2 = SubmitField('Επιλογή Καταλύματος')



class AddHouseForm(FlaskForm):
    house_name = StringField('Όνομα Σπιτιού')
    city = StringField('Πόλη')
    postal_code = IntegerField('Ταχυδρομικός Κώδικας')
    address = StringField('Διεύθυνση')
    square_meters = IntegerField('Τετραγωνικά Μέτρα')
    price = IntegerField('Τιμή')
    house_type = StringField('Είδος Καταλύματος')
    visitors = IntegerField('Επισκέπτες')
    submit = SubmitField('Αποθήκευση')

class UpdateHouseForm(FlaskForm):
    house_name = StringField('Όνομα Σπιτιού')
    city = StringField('Πόλη')
    postal_code = IntegerField('Ταχυδρομικός Κώδικας')
    address = StringField('Διεύθυνση')
    square_meters = IntegerField('Τετραγωνικά Μέτρα')
    price = IntegerField('Τιμή')
    house_type = StringField('Είδος Καταλύματος')
    visitors = IntegerField('Επισκέπτες')
    picture = FileField('Ενημέρωση Εικόνας Προφίλ', validators=[FileAllowed(['jpg', 'png'])])
    house_id = IntegerField('Id Σπιτιού')
    submit = SubmitField('Αποθήκευση')


class HouseSelectForm(FlaskForm):
    house_id = IntegerField('Id Σπιτιού')
    submit = SubmitField('Επεξεργασία')


class SearchForm(FlaskForm):
    location = StringField('Περιοχή')
    arrival_date = DateField('Ημερομηνία Άφιξης', format='%Y-%m-%d')
    guests = IntegerField('Αριθμός Επισκεπτών')
    submit = SubmitField('Αναζήτηση')
    house_id = IntegerField('Id Σπιτιού')
    submit2 = SubmitField('Κάντε Κράτηση')

class ResultsForm(FlaskForm):
    submit = SubmitField('Κάντε Κράτηση')



