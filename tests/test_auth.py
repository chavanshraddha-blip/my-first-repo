import pytest
from app.models.user import User
from app.extensions import db


def test_user_password_hashing(app):
    with app.app_context():
        user = User(username='hashuser', email='hash@example.com')
        user.set_password('mysecretpass')
        assert user.password_hash is not None
        assert user.password_hash != 'mysecretpass'
        assert user.check_password('mysecretpass') is True
        assert user.check_password('wrongpass') is False


def test_registration_success(client, auth, app):
    response = auth.register(
        username='newauthor',
        email='newauthor@example.com',
        password='strongpassword',
        confirm_password='strongpassword'
    )
    assert response.status_code == 200
    assert b'Your account has been created successfully' in response.data

    with app.app_context():
        user = User.query.filter_by(username='newauthor').first()
        assert user is not None
        assert user.email == 'newauthor@example.com'


def test_registration_duplicate_username(client, auth):
    auth.register(username='duplicateuser', email='dup1@example.com')
    response = auth.register(username='duplicateuser', email='dup2@example.com')
    assert b'This username is already taken' in response.data


def test_registration_duplicate_email(client, auth):
    auth.register(username='userone', email='same@example.com')
    response = auth.register(username='usertwo', email='same@example.com')
    assert b'An account with this email already exists' in response.data


def test_registration_password_mismatch(client, auth):
    response = auth.register(
        username='mismatchuser',
        email='mismatch@example.com',
        password='password123',
        confirm_password='differentpassword'
    )
    assert b'Passwords must match' in response.data


def test_login_with_username_success(client, auth):
    auth.register(username='loginuser', email='loginuser@example.com', password='secretpassword', confirm_password='secretpassword')
    response = auth.login(login_id='loginuser', password='secretpassword')
    assert response.status_code == 200
    assert b'Welcome back, loginuser!' in response.data


def test_login_with_email_success(client, auth):
    auth.register(username='emailuser', email='emailuser@example.com', password='secretpassword', confirm_password='secretpassword')
    response = auth.login(login_id='emailuser@example.com', password='secretpassword')
    assert response.status_code == 200
    assert b'Welcome back, emailuser!' in response.data


def test_login_invalid_password(client, auth):
    auth.register(username='wrongpassuser', email='wrongpass@example.com', password='secretpassword', confirm_password='secretpassword')
    response = auth.login(login_id='wrongpassuser', password='incorrect')
    assert b'Invalid username/email or password' in response.data


def test_logout(client, auth):
    auth.register(username='logoutuser', email='logout@example.com', password='secretpassword', confirm_password='secretpassword')
    auth.login(login_id='logoutuser', password='secretpassword')
    response = auth.logout()
    assert response.status_code == 200
    assert b'You have been logged out safely' in response.data


def test_login_required_protection(client):
    response = client.get('/posts/create', follow_redirects=True)
    assert b'Please log in to access this page' in response.data
    assert b'Sign In' in response.data
