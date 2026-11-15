from urllib.parse import urlparse
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models.user import User
from app.auth.forms import RegistrationForm, LoginForm, EditProfileForm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip().lower()
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created successfully! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title='Register', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        login_val = form.login_id.data.strip()
        user = User.query.filter(
            (User.username == login_val) | (User.email == login_val.lower())
        ).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash(f'Welcome back, {user.username}!', 'success')
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('main.index')
            return redirect(next_page)
        else:
            flash('Invalid username/email or password. Please try again.', 'danger')

    return render_template('auth/login.html', title='Login', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out safely.', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = EditProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data.strip()
        current_user.bio = form.bio.data.strip() if form.bio.data else ''

        if form.new_password.data:
            if not current_user.check_password(form.current_password.data):
                flash('Incorrect current password. Password was not changed.', 'danger')
                return render_template('auth/profile.html', title='My Profile', form=form)
            current_user.set_password(form.new_password.data)
            flash('Password updated successfully!', 'success')

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('auth.profile'))

    return render_template('auth/profile.html', title='My Profile', form=form)
