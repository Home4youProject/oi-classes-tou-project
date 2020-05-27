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
