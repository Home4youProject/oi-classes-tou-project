@app.route("/edit_house", methods=['GET', 'POST'])
@login_required
def edit_house():
    form = UpdateHouseForm()
    house = House.query.filter_by(user_id=current_user.id).first_or_404()
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
