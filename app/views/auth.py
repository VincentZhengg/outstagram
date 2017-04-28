import json
import uuid
import os
import random
import string

from flask import Blueprint, render_template, redirect, request, \
    url_for, flash, Response, jsonify, current_app, session, abort
from flask_login import login_user, logout_user, login_required, \
    current_user
from captcha.image import ImageCaptcha

from app.extensions import db
from app.models import User
from app.email import send_email
from app.forms import LoginForm, RegistrationForm


auth = Blueprint('auth', __name__)


@auth.errorhandler(404)
def page_not_found(error):
    return render_template("errors/auth404.html", error=error)


def generate_random_chars(length=4):
    char = ''
    for i in range(length):
        char += random.choice(string.ascii_lowercase.replace("o", "") + string.digits.replace("0", ""))
    return char


def generate_img_name():
    unique_id = str(uuid.uuid4())
    return "captcha_{}.png".format(unique_id)


def generate_captcha(chars):
    image = ImageCaptcha()
    image_name = generate_img_name()
    image.write(chars, os.path.join(current_app.config['CAPTCHA_DIR'], image_name))
    return image_name


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if request.endpoint is None:
            abort(404)
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/validate/password', methods=['POST'])
def validate_password():
    email = request.form.get("email")
    password = request.form.get("password")
    user = User.query.filter_by(email=email).first()
    if user is not None and user.verify_password(password):
        return Response(json.dumps(True), headers={"content-type": "application/json"})
    else:
        return Response(json.dumps(False), headers={"content-type": "application/json"})


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(formdata=request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid email or password.')

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(formdata=request.form)
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        flash("register successfully")
        return redirect(url_for('main.index'))
    return render_template('auth/signup.html', form=form)


@auth.route('/captcha')
def captcha():
    chars = generate_random_chars()
    image_name = generate_captcha(chars=chars)
    session['captcha'] = chars
    return jsonify({'img_url': os.path.join("/static/captcha", image_name)})


@auth.route('/verify/captcha')
def verify_captcha():
    cli_code = request.args.get("captcha")
    svr_code = session.get("captcha")
    if not cli_code:
        return Response(json.dumps(False), headers={"content-type": "application/json"})
    if svr_code.lower() == cli_code.lower():
        return Response(json.dumps(True), headers={"content-type": "application/json"})
    else:
        return Response(json.dumps(False), headers={"content-type": "application/json"})


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.route('/validate/email')
def validate_email():
    email = request.args.get("email")
    if User.query.filter_by(email=email).first():
        return Response(json.dumps(False), headers={"content-type": "application/json"})
    else:
        return Response(json.dumps(True), headers={"content-type": "application/json"})


@auth.route('/validate/username')
def validate_username():
    username = request.args.get("username")
    if User.query.filter_by(username=username).first():
        return Response(json.dumps(False), headers={"content-type": "application/json"})
    else:
        return Response(json.dumps(True), headers={"content-type": "application/json"})
