from flask import Blueprint, render_template, request

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register')
def register():
    return render_template('register.html')

@auth_bp.route('/login')
def login():
    return "Login Page (to be implemented)"

@auth_bp.route('/error')
def error():
    error_message = request.args.get('message', 'An unknown error occurred.')
    return render_template('error.html', error_message=error_message)
