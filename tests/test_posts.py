import pytest
from app.models.post import Post
from app.models.category import Category
from app.models.tag import Tag
from app.models.user import User
from app.extensions import db


def test_create_post(client, auth, app):
    auth.register(username='writer', email='writer@example.com')
    auth.login(login_id='writer')

    with app.app_context():
        cat = Category.query.first()
        cat_id = cat.id

    response = client.post('/posts/create', data={
        'title': 'How to Build Flask Applications',
        'category_id': cat_id,
        'tags': 'flask, python, architecture',
        'summary': 'A complete guide to Flask',
        'content': '<p>This is the full rich text body of the tutorial.</p>'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Your blog post has been published successfully!' in response.data
    assert b'How to Build Flask Applications' in response.data

    with app.app_context():
        post = Post.query.filter_by(title='How to Build Flask Applications').first()
        assert post is not None
        assert post.author.username == 'writer'
        assert len(post.tags) == 3
        tag_names = [t.name for t in post.tags]
        assert 'flask' in tag_names
        assert 'python' in tag_names


def test_post_detail_view(client, sample_post):
    response = client.get(f'/posts/{sample_post}')
    assert response.status_code == 200
    assert b'Sample Post for Testing' in response.data
    assert b'This is the test content of the blog post' in response.data


def test_edit_post_by_author(client, auth, app, sample_post):
    auth.login(login_id='author1', password='securepassword')

    response = client.post(f'/posts/{sample_post}/edit', data={
        'title': 'Updated Title for Testing',
        'category_id': 1,
        'tags': 'flask, updated',
        'summary': 'Updated summary',
        'content': '<p>Updated content body</p>'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Your post has been updated successfully!' in response.data
    assert b'Updated Title for Testing' in response.data

    with app.app_context():
        post = db.session.get(Post, sample_post)
        assert post.title == 'Updated Title for Testing'


def test_edit_post_unauthorized_by_different_user(client, auth, sample_post):
    # Register and login as different user
    auth.register(username='intruder', email='intruder@example.com', password='password123', confirm_password='password123')
    auth.login(login_id='intruder', password='password123')

    # Attempt to edit author1's post
    response = client.post(f'/posts/{sample_post}/edit', data={
        'title': 'Hacked Title',
        'category_id': 1,
        'tags': 'hacked',
        'content': '<p>Hacked</p>'
    }, follow_redirects=True)

    assert response.status_code == 403


def test_delete_post_by_author(client, auth, app, sample_post):
    auth.login(login_id='author1', password='securepassword')

    response = client.post(f'/posts/{sample_post}/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b'The blog post has been deleted' in response.data

    with app.app_context():
        post = db.session.get(Post, sample_post)
        assert post is None


def test_delete_post_unauthorized(client, auth, app, sample_post):
    auth.register(username='otheruser', email='other@example.com', password='password123', confirm_password='password123')
    auth.login(login_id='otheruser', password='password123')

    response = client.post(f'/posts/{sample_post}/delete', follow_redirects=True)
    assert response.status_code == 403

    with app.app_context():
        post = db.session.get(Post, sample_post)
        assert post is not None
