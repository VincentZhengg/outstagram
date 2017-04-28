from flask import Blueprint, render_template, current_app


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/error')
def myerror():
    # print(current_app.config['DEBUG'])
    a = []
    name = a[1]
    return render_template('index.html')