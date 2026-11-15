import os
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.post import Post, post_tags
from app.models.category import Category
from app.models.tag import Tag
from app.models.comment import Comment

app = create_app(os.environ.get('FLASK_CONFIG', 'development'))


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Post': Post,
        'Category': Category,
        'Tag': Tag,
        'Comment': Comment,
        'post_tags': post_tags
    }


@app.cli.command('init-db')
def init_db_command():
    """Create database tables and seed initial categories."""
    db.create_all()
    seed_initial_data()
    print("Database tables initialized and seeded successfully.")


def seed_initial_data():
    """Seed initial categories and demo data if not already present."""
    default_categories = [
        ('Technology', 'tech', 'Latest trends in tech, software engineering, and AI.'),
        ('Web Development', 'web-dev', 'Tutorials and guides on full-stack web development.'),
        ('Python & Flask', 'python-flask', 'Deep dives into Python, Flask, and backend architectures.'),
        ('Design & UX', 'design-ux', 'UI/UX best practices, typography, and responsive design.'),
        ('Career & Internship', 'career', 'Advice, interview tips, and internship experiences.')
    ]

    for name, slug, desc in default_categories:
        if not Category.query.filter_by(slug=slug).first():
            cat = Category(name=name, slug=slug, description=desc)
            db.session.add(cat)

    default_tags = ['python', 'flask', 'webdev', 'javascript', 'html', 'css', 'internship', 'tutorial']
    for tag_name in default_tags:
        if not Tag.query.filter_by(name=tag_name).first():
            tag = Tag(name=tag_name, slug=tag_name)
            db.session.add(tag)

    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_initial_data()
    app.run(host='127.0.0.1', port=5000, debug=True)
