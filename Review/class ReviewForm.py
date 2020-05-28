class ReviewForm(FlaskForm):
    reviewer = IntegerField('Reviewer')
    recipient = IntegerField('Id')
    stars = IntegerField('Stars')
    comments = StringField('Comments')
    submit = SubmitField('Προσθήκη Αξιολόγησης')
    submit2 = SubmitField('Επιλογή Καταλύματος')