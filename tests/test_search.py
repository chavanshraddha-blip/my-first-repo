import pytest
from app.models.post import Post
from app.models.category import Category
from app.models.tag import Tag
from app.models.user import User
from app.extensions import db


@pytest.fixture
def search_dataset(app):
    with app.app_context():
        author = User(username='searchauthor', email='searchauthor@example.com')
        author.set_password('pass123')
        db.session.add(author)
        db.session.commit()

        cat_web = Category.query.filter_by(slug='technology').first()
        cat_tut = Category.query.filter_by(slug='tutorials').first()

        tag_python = Tag.query.filter_by(slug='python').first()
        tag_flask = Tag.query.filter_by(slug='flask').first()

        p1 = Post(
            title='Learning Python Async Programming',
            slug='learning-python-async',
            content='Deep dive into asyncio, coroutines, and event loops in modern Python.',
            summary='Mastering Python async',
            author=author,
            category=cat_web
        )
        p1.tags.append(tag_python)

        p2 = Post(
            title='Building Web APIs with Flask',
            slug='building-web-apis-flask',
            content='Step by step guide to creating RESTful endpoints and serializing JSON.',
            summary='Flask REST API guide',
            author=author,
            category=cat_tut
        )
        p2.tags.append(tag_flask)
        p2.tags.append(tag_python)

        p3 = Post(
            title='Deploying Containerized Applications',
            slug='deploying-containerized-apps',
            content='Using Docker, multi-stage builds, and Kubernetes orchestration.',
            summary='Docker guide',
            author=author,
            category=cat_web
        )

        db.session.add_all([p1, p2, p3])
        db.session.commit()


def test_search_by_title(client, search_dataset):
    response = client.get('/?q=Async')
    assert response.status_code == 200
    assert b'Learning Python Async Programming' in response.data
    assert b'Building Web APIs with Flask' not in response.data


def test_search_by_content(client, search_dataset):
    response = client.get('/?q=RESTful')
    assert response.status_code == 200
    assert b'Building Web APIs with Flask' in response.data
    assert b'Learning Python Async Programming' not in response.data


def test_filter_by_category(client, search_dataset):
    response = client.get('/?category=tutorials')
    assert response.status_code == 200
    assert b'Building Web APIs with Flask' in response.data
    assert b'Learning Python Async Programming' not in response.data


def test_filter_by_tag(client, search_dataset):
    response = client.get('/?tag=flask')
    assert response.status_code == 200
    assert b'Building Web APIs with Flask' in response.data
    assert b'Deploying Containerized Applications' not in response.data


def test_combined_search_and_category(client, search_dataset):
    # Searching 'Python' inside 'technology' category matches p1, but not p2 (which is in 'tutorials')
    response = client.get('/?q=Python&category=technology')
    assert response.status_code == 200
    assert b'Learning Python Async Programming' in response.data
    assert b'Building Web APIs with Flask' not in response.data


def test_search_no_results(client, search_dataset):
    response = client.get('/?q=NonExistentKeywordXYZ')
    assert response.status_code == 200
    assert b'No articles found' in response.data
