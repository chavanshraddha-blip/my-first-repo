import pytest
from app.models.comment import Comment
from app.models.post import Post
from app.extensions import db


def test_add_comment_authenticated(client, auth, app, sample_post):
    auth.register(username='commenter', email='commenter@example.com')
    auth.login(login_id='commenter')

    response = client.post(f'/comments/post/{sample_post}/add', data={
        'content': 'This is a fantastic and insightful article!'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Your comment has been added' in response.data
    assert b'This is a fantastic and insightful article!' in response.data

    with app.app_context():
        comment = Comment.query.filter_by(content='This is a fantastic and insightful article!').first()
        assert comment is not None
        assert comment.author.username == 'commenter'
        assert comment.post_id == sample_post


def test_add_comment_unauthenticated(client, sample_post):
    response = client.post(f'/comments/post/{sample_post}/add', data={
        'content': 'Unauthenticated comment'
    }, follow_redirects=True)

    assert b'Please log in to access this page' in response.data


def test_delete_comment_by_comment_author(client, auth, app, sample_post):
    auth.register(username='commenter2', email='commenter2@example.com')
    auth.login(login_id='commenter2')

    client.post(f'/comments/post/{sample_post}/add', data={
        'content': 'Comment to be removed soon'
    }, follow_redirects=True)

    with app.app_context():
        comment = Comment.query.filter_by(content='Comment to be removed soon').first()
        comment_id = comment.id

    response = client.post(f'/comments/{comment_id}/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'Comment removed successfully' in response.data

    with app.app_context():
        deleted = db.session.get(Comment, comment_id)
        assert deleted is None


def test_delete_comment_unauthorized(client, auth, app, sample_post):
    auth.register(username='userA', email='userA@example.com')
    auth.login(login_id='userA')
    client.post(f'/comments/post/{sample_post}/add', data={
        'content': 'User A secret comment'
    }, follow_redirects=True)

    with app.app_context():
        comment = Comment.query.filter_by(content='User A secret comment').first()
        comment_id = comment.id

    # Log in as userB (neither author of post nor comment)
    auth.register(username='userB', email='userB@example.com')
    auth.login(login_id='userB')

    response = client.post(f'/comments/{comment_id}/delete', follow_redirects=True)
    assert response.status_code == 403

    with app.app_context():
        comment = db.session.get(Comment, comment_id)
        assert comment is not None


def test_post_author_can_delete_any_comment_on_their_post(client, auth, app, sample_post):
    # Register commenter and leave a comment
    auth.register(username='spammer', email='spammer@example.com')
    auth.login(login_id='spammer')
    client.post(f'/comments/post/{sample_post}/add', data={
        'content': 'Spam comment on post'
    }, follow_redirects=True)

    with app.app_context():
        comment = Comment.query.filter_by(content='Spam comment on post').first()
        comment_id = comment.id

    # Log in as author1 (post author)
    auth.login(login_id='author1', password='securepassword')
    response = client.post(f'/comments/{comment_id}/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'Comment removed successfully' in response.data

    with app.app_context():
        comment = db.session.get(Comment, comment_id)
        assert comment is None
