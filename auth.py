from flask import Blueprint, request, render_template, flash, redirect, url_for,session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                email_part = email.split('@')
                if len(email_part) !=2 :
                    return "Invalid email address format"
                domain = email_part[1]
                if domain == 'hcl.com':
                    session['user_type'] = 'hcl'
                elif domain == 'admin.com':
                    session['user_type'] = 'admin'
                elif domain == 'vendor.com':
                    session['user_type'] = 'vendor'
                
                else:
                    return "Unknown Domain"
                
                login_user(user, remember=True)

                if session['user_type'] == 'hcl':
                    return redirect(url_for('routes.home'))
                elif session['user_type'] == 'admin':
                    return redirect(url_for('routes.admin'))
                elif session['user_type'] == 'vendor':
                    return redirect(url_for('routes.vendor'))
            else:
                flash('Incorrect Password', category='error')   
        else:
            flash('Email does not exist', category='error')

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up',methods = ['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists',category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 chars', category='error')
        elif len(password1) < 7:
            flash('Password must be greater than 7 chars and more complex', category='error')
        elif len(password2) < 7:
            flash('Password must be greater than 7 chars and more complex', category='error')
        elif(password1 != password2):
            flash('Passwords dont match',category='error')
        else:
            new_user = User(email=email, password = generate_password_hash(password1, method='pbkdf2:sha1', salt_length=8))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created Successfully', category='succes')
            return redirect(url_for('auth.login'))
        
    return render_template('signup.html')