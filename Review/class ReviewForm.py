class ReviewForm(FlaskForm):
    reviewer = IntegerField('Reviewer')
    recipient = IntegerField('Id')
    stars = IntegerField('Stars')
    comments = StringField('Comments')
    submit = SubmitField('�������� �����������')
    submit2 = SubmitField('������� �����������')