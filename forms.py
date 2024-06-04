# paperbackcollections/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, NumberRange

class CheckoutForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Place Order')
