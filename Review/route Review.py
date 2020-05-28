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