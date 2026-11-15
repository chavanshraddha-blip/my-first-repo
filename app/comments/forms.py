from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class CommentForm(FlaskForm):
    content = TextAreaField(
        'Leave a Comment',
        validators=[
            DataRequired(message='Comment cannot be empty.'),
            Length(min=2, max=1000, message='Comment must be between 2 and 1000 characters.')
        ]
    )
    submit = SubmitField('Post Comment')
