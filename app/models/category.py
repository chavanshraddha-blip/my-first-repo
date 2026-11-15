from app.extensions import db


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(60), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255), default='')

    # Relationships
    posts = db.relationship('Post', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'<Category {self.name}>'
