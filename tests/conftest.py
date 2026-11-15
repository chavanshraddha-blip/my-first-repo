import pytest
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.category import Category
from app.models.tag import Tag
from app.models.post import Post


@pytest.fixture
def app():
    app = create_app('testing')

    with app.app_context():
        db.create_all()

        # Seed categories for testing
        cat1 = Category(name='Technology', slug='technology', description='Tech articles')
        cat2 = Category(name='Tutorials', slug='tutorials', description='Guides and walkthroughs')
        db.session.add_all([cat1, cat2])

        # Seed tags
        tag1 = Tag(name='python', slug='python')
        tag2 = Tag(name='flask', slug='flask')
        db.session.add_all([tag1, tag2])

        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions:
    def __init__(self, client):
        self._client = client

    def register(self, username='testuser', email='test@example.com', password='password123', confirm_password='password123'):
        self._client.get('/auth/logout', follow_redirects=True)
        return self._client.post('/auth/register', data={
            'username': username,
            'email': email,
            'password': password,
            'confirm_password': confirm_password
        }, follow_redirects=True)

    def login(self, login_id='testuser', password='password123', remember_me=False):
        self._client.get('/auth/logout', follow_redirects=True)
        return self._client.post('/auth/login', data={
            'login_id': login_id,
            'password': password,
            'remember_me': remember_me
        }, follow_redirects=True)

    def logout(self):
        return self._client.get('/auth/logout', follow_redirects=True)


@pytest.fixture
def auth(client):
    return AuthActions(client)


@pytest.fixture
def sample_user(app):
    with app.app_context():
        user = User(username='author1', email='author1@example.com', bio='Software Engineer')
        user.set_password('securepassword')
        db.session.add(user)
        db.session.commit()
        return user.id


@pytest.fixture
def sample_post(app, sample_user):
    with app.app_context():
        cat = Category.query.filter_by(slug='technology').first()
        tag = Tag.query.filter_by(slug='flask').first()
        post = Post(
            title='Sample Post for Testing',
            slug='sample-post-for-testing',
            content='<p>This is the test content of the blog post.</p>',
            summary='Test summary',
            user_id=sample_user,
            category_id=cat.id
        )
        post.tags.append(tag)
        db.session.add(post)
        db.session.commit()
        return post.id
