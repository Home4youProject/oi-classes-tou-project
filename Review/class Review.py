class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reviewer = db.Column(db.Integer, nullable=False)
    recipient = db.Column(db.Integer(), nullable=False)
    stars = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.String(200))