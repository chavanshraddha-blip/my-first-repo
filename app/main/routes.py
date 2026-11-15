from flask import Blueprint, render_template, request, current_app
from sqlalchemy import or_
from app.models.user import User
from app.models.post import Post
from app.models.category import Category
from app.models.tag import Tag

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('q', '', type=str).strip()
    category_slug = request.args.get('category', '', type=str).strip()
    tag_slug = request.args.get('tag', '', type=str).strip()
    sort_by = request.args.get('sort', 'newest', type=str).strip()

    per_page = current_app.config.get('POSTS_PER_PAGE', 5)
    query = Post.query

    # Search filter (Week 6: search by title or content)
    if search_query:
        search_term = f"%{search_query}%"
        query = query.filter(
            or_(
                Post.title.ilike(search_term),
                Post.content.ilike(search_term),
                Post.summary.ilike(search_term)
            )
        )

    # Category filter
    active_category = None
    if category_slug:
        active_category = Category.query.filter_by(slug=category_slug).first()
        if active_category:
            query = query.filter(Post.category_id == active_category.id)

    # Tag filter
    active_tag = None
    if tag_slug:
        active_tag = Tag.query.filter_by(slug=tag_slug).first()
        if active_tag:
            query = query.filter(Post.tags.contains(active_tag))

    # Sorting
    if sort_by == 'oldest':
        query = query.order_by(Post.created_at.asc())
    else:
        query = query.order_by(Post.created_at.desc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    posts = pagination.items

    # Featured / Latest 3 posts for carousel / banner if on page 1 without search
    featured_posts = []
    if page == 1 and not search_query and not category_slug and not tag_slug:
        featured_posts = Post.query.order_by(Post.created_at.desc()).limit(3).all()

    all_categories = Category.query.order_by(Category.name.asc()).all()
    all_tags = Tag.query.order_by(Tag.name.asc()).limit(20).all()

    return render_template(
        'main/index.html',
        title='Home - Modern Blogging Platform',
        pagination=pagination,
        posts=posts,
        featured_posts=featured_posts,
        categories=all_categories,
        tags=all_tags,
        search_query=search_query,
        category_slug=category_slug,
        tag_slug=tag_slug,
        sort_by=sort_by,
        active_category=active_category,
        active_tag=active_tag
    )


@main_bp.route('/user/<username>')
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('POSTS_PER_PAGE', 5)

    pagination = user.posts.order_by(Post.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'main/user_profile.html',
        title=f'{user.username} - Profile',
        user=user,
        pagination=pagination,
        posts=pagination.items
    )


@main_bp.route('/about')
def about():
    total_posts = Post.query.count()
    total_users = User.query.count()
    total_categories = Category.query.count()
    return render_template(
        'main/about.html',
        title='About the Platform',
        stats={
            'posts': total_posts,
            'users': total_users,
            'categories': total_categories
        }
    )
