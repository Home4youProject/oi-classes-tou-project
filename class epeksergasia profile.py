class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    phone = IntegerField('Phone Number')
    birth_date = DateField('Date of birth', format='%Y-%m-%d')
    firstname = StringField('Name')
    surname = StringField('Surname')
    sex = StringField('Sex')
    submit = SubmitField('Update')