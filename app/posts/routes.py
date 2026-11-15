from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, current_app
from flask_login import login_required, current_user
from app.extensions import db
from app.models.post import Post
from app.models.category import Category
from app.models.tag import Tag
from app.posts.forms import PostForm
from app.comments.forms import CommentForm
from app.utils import clean_html, generate_slug

posts_bp = Blueprint('posts', __name__)


def sync_post_tags(post, tags_string):
    """Parse comma-separated tag string and update post tags relationship."""
    post.tags.clear()
    if not tags_string:
        return

    tag_names = [t.strip().lower() for t in tags_string.split(',') if t.strip()]
    unique_tags = list(dict.fromkeys(tag_names))

    for name in unique_tags:
        slug = generate_slug(name)
        tag = Tag.query.filter_by(name=name).first()
        if not tag:
            tag = Tag(name=name, slug=slug or name)
            db.session.add(tag)
        post.tags.append(tag)


@posts_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    categories = Category.query.order_by(Category.name.asc()).all()
    form.category_id.choices = [(c.id, c.name) for c in categories]

    if form.validate_on_submit():
        slug = generate_slug(form.title.data)
        sanitized_content = clean_html(form.content.data)

        # Auto-generate summary from content if not provided
        summary = form.summary.data.strip() if form.summary.data else ''
        if not summary:
            import re
            plain_text = re.sub('<[^<]+?>', '', sanitized_content)
            summary = (plain_text[:200] + '...') if len(plain_text) > 200 else plain_text

        post = Post(
            title=form.title.data.strip(),
            slug=slug,
            content=sanitized_content,
            summary=summary,
            category_id=form.category_id.data,
            author=current_user
        )
        db.session.add(post)
        sync_post_tags(post, form.tags.data)

        db.session.commit()
        flash('Your blog post has been published successfully!', 'success')
        return redirect(url_for('posts.post_detail', post_id=post.id))

    return render_template('posts/create_post.html', title='Create New Post', form=form)


@posts_bp.route('/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    comment_form = CommentForm()
    # Fetch related posts from same category
    related_posts = Post.query.filter(
        Post.category_id == post.category_id,
        Post.id != post.id
    ).order_by(Post.created_at.desc()).limit(3).all()

    return render_template(
        'posts/post_detail.html',
        title=post.title,
        post=post,
        comment_form=comment_form,
        related_posts=related_posts
    )


@posts_bp.route('/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Ownership check
    if post.author != current_user:
        flash('You are not authorized to edit this post.', 'danger')
        abort(403)

    form = PostForm()
    categories = Category.query.order_by(Category.name.asc()).all()
    form.category_id.choices = [(c.id, c.name) for c in categories]

    if form.validate_on_submit():
        post.title = form.title.data.strip()
        post.slug = generate_slug(form.title.data)
        post.content = clean_html(form.content.data)
        post.summary = form.summary.data.strip() if form.summary.data else post.summary
        post.category_id = form.category_id.data
        sync_post_tags(post, form.tags.data)

        db.session.commit()
        flash('Your post has been updated successfully!', 'success')
        return redirect(url_for('posts.post_detail', post_id=post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.category_id.data = post.category_id
        form.summary.data = post.summary
        form.content.data = post.content
        form.tags.data = post.tags_as_string

    return render_template('posts/edit_post.html', title=f'Edit: {post.title}', form=form, post=post)


@posts_bp.route('/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Ownership check
    if post.author != current_user:
        flash('You are not authorized to delete this post.', 'danger')
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('The blog post has been deleted.', 'info')
    return redirect(url_for('main.index'))


@posts_bp.route('/category/<slug>')
def category_posts(slug):
    category = Category.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('POSTS_PER_PAGE', 5)

    pagination = Post.query.filter_by(category=category)\
        .order_by(Post.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'posts/category_posts.html',
        title=f'Category: {category.name}',
        category=category,
        pagination=pagination,
        posts=pagination.items
    )


@posts_bp.route('/tag/<slug>')
def tag_posts(slug):
    tag = Tag.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('POSTS_PER_PAGE', 5)

    pagination = tag.posts.order_by(Post.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'posts/tag_posts.html',
        title=f'Tag: #{tag.name}',
        tag=tag,
        pagination=pagination,
        posts=pagination.items
    )


@posts_bp.route('/my-posts')
@login_required
def my_posts():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config.get('POSTS_PER_PAGE', 8)

    pagination = current_user.posts.order_by(Post.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        'posts/my_posts.html',
        title='My Blog Posts',
        pagination=pagination,
        posts=pagination.items
    )
