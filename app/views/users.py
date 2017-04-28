from flask import Blueprint, abort, render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user

from app.forms import EditProfileForm
from app.models import User
from app.extensions import db, photos
from PIL import Image


users = Blueprint('users', __name__, url_prefix='user')


@users.route('/<username>')
def user_profile(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('users/user.html', user=user)


@users.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('users.user_profile', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('users/edit_profile.html', form=form)


@users.route('/<username>/upload-image',  methods=['POST'])
def upload_image(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    if request.method == 'POST' and 'photo' in request.files:
        crop_x = request.form.get('cropx')
        crop_y = request.form.get('cropy')
        crop_w = request.form.get('cropw')
        crop_h = request.form.get('croph')
        photos.save(request.files['photo'])
        flash("Photo saved.")
    return render_template('users/user.html', user=user)