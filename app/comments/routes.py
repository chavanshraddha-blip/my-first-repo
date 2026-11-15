from flask import Blueprint, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models.post import Post
from app.models.comment import Comment
from app.comments.forms import CommentForm
from app.utils import clean_html

comments_bp = Blueprint('comments', __name__)


@comments_bp.route('/post/<int:post_id>/add', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()

    if form.validate_on_submit():
        cleaned_content = clean_html(form.content.data.strip())
        comment = Comment(
            content=cleaned_content,
            author=current_user,
            post=post
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added.', 'success')
        return redirect(url_for('posts.post_detail', post_id=post.id, _anchor=f'comment-{comment.id}'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(error, 'danger')
        return redirect(url_for('posts.post_detail', post_id=post.id, _anchor='comments-section'))


@comments_bp.route('/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    post_id = comment.post_id

    # The comment author or the post owner can delete the comment
    if comment.author != current_user and comment.post.author != current_user:
        flash('You are not authorized to delete this comment.', 'danger')
        abort(403)

    db.session.delete(comment)
    db.session.commit()
    flash('Comment removed successfully.', 'info')
    return redirect(url_for('posts.post_detail', post_id=post_id, _anchor='comments-section'))
