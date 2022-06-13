from colorama import reinit
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import *
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import crypt

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect login, try again.', category='error')
        else:
            flash('Account does not exist please sign up.', category='error')

    return render_template("login.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email = email).first()
        if user:
            flash('Account already created', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category="error")
        elif len(firstname) < 2:
            flash('First name must be greater than 1 characters.', category="error")
        elif password1 != password2:
            flash('Passwords don\'t match.', category="error")
        elif len(password1) < 7:
            flash('password must be greater than 6 characters.', category="error")
        else:
            new_user = User(email=email, firstname=firstname, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created!', category="success")
            return redirect(url_for('views.home'))
    return render_template("signup.html")