import os
from flask import Flask, render_template
from config import config
from app.extensions import db, migrate, login_manager, csrf


def create_app(config_name=None):
    """Application factory for the Blogging Platform."""
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Ensure the instance directory exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Register Blueprints
    from app.main.routes import main_bp
    from app.auth.routes import auth_bp
    from app.posts.routes import posts_bp
    from app.comments.routes import comments_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(posts_bp, url_prefix='/posts')
    app.register_blueprint(comments_bp, url_prefix='/comments')

    # Global context processors for template access
    from app.models.category import Category
    from app.models.tag import Tag

    @app.context_processor
    def inject_global_data():
        try:
            categories = Category.query.order_by(Category.name.asc()).all()
            popular_tags = Tag.query.limit(10).all()
        except Exception:
            categories = []
            popular_tags = []
        return dict(nav_categories=categories, nav_tags=popular_tags)

    # Error Handlers
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    # Custom Jinja filters
    @app.template_filter('datetime_format')
    def datetime_format_filter(value, format='%b %d, %Y'):
        if value is None:
            return ''
        return value.strftime(format)

    return app
