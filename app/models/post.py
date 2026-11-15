import math
import re
from datetime import datetime
from app.extensions import db

post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(180), index=True)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String(300), default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)

    # Many-to-Many Tags
    tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts', lazy='dynamic'), lazy='subquery')

    # Comments relationship
    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade='all, delete-orphan', order_by='Comment.created_at.desc()')

    @property
    def reading_time(self):
        """Estimate reading time in minutes."""
        # Strip HTML tags
        clean_text = re.sub('<[^<]+?>', '', self.content or '')
        words = len(clean_text.split())
        minutes = math.ceil(words / 200)
        return max(1, minutes)

    @property
    def tags_as_string(self):
        """Comma-separated tags for form prefilling."""
        return ', '.join([t.name for t in self.tags])

    def __repr__(self):
        return f'<Post "{self.title}">'
