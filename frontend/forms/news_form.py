from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField, IntegerField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.simple import HiddenField
from wtforms.validators import DataRequired, Length
from flask_quill.fields.wysiwyg import WysiwygField



class NewsForm(FlaskForm):
    delta = HiddenField(
        'delta',
        validators=[Length(0, 255)],
    )
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    source_type = StringField('Source Type', validators=[DataRequired()])
    tags = SelectField('Tags', coerce=int)  # Используем coerce=int для преобразования значений в целые числа
    submit = SubmitField('Submit')
