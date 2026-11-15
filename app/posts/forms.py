from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class PostForm(FlaskForm):
    title = StringField(
        'Post Title',
        validators=[
            DataRequired(message='Title is required.'),
            Length(min=3, max=150, message='Title must be between 3 and 150 characters.')
        ]
    )
    category_id = SelectField(
        'Category',
        coerce=int,
        validators=[DataRequired(message='Please select a category.')]
    )
    tags = StringField(
        'Tags (comma separated, e.g. python, web, flask)',
        validators=[Optional(), Length(max=150)]
    )
    summary = TextAreaField(
        'Summary / Excerpt (Optional short preview)',
        validators=[Optional(), Length(max=300, message='Summary cannot exceed 300 characters.')]
    )
    content = TextAreaField(
        'Content',
        validators=[DataRequired(message='Post content cannot be empty.')]
    )
    submit = SubmitField('Publish Post')
