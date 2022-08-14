from wtforms import Form, StringField, IntegerField, SelectField, DateTimeField
from wtforms.validators import DataRequired

# Config CSRF


class ActorForm(Form):
    name = StringField('name', validators=[DataRequired()])
    age = IntegerField('age', validators=[DataRequired()])
    gender = SelectField('gender', choices=['Male', 'Female'])


class MovieForm(Form):
    title = StringField('movie', validators=[DataRequired()])
    release_date = DateTimeField('release_date', validators=[DataRequired()])
