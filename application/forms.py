from datetime import date

from flask_wtf import Form
from wtforms import (
    StringField,
    HiddenField,
    BooleanField,
    DateField,
    SubmitField,
    SelectField,
    RadioField,
    TextAreaField,
    IntegerField
)

from wtforms.validators import DataRequired, ValidationError, NumberRange, Email


class ValidateDateNotInFuture(object):
    def __init__(self):
        self.message = "The date must not be in the future"

    def __call__(self, form, field):
        self._validate_date_not_in_future(form, field.data)

    def _validate_date_not_in_future(self, form, date_field):
        if date_field > date.today():
            raise ValidationError('Date cannot be in the future')

class DebtorForm(Form):

    forename = StringField('Forename', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    alt_forename = StringField('Alternative forename', validators=[DataRequired()])
    alt_surname = StringField('Alternative surname', validators=[DataRequired()])
    dob = StringField('Date of birth', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    occupation = StringField('Occupation', validators=[DataRequired()])
    trading = StringField('Trading name', validators=[DataRequired()])

class AddressForm(DebtorForm):
    addressList = []
    forename = HiddenField('Forename', validators=[DataRequired()])
    surname = HiddenField('Surname', validators=[DataRequired()])
    alt_forename = HiddenField('Alternative forename', validators=[DataRequired()])
    alt_surname = HiddenField('Alternative surname', validators=[DataRequired()])
    dob = HiddenField('Date of birth', validators=[DataRequired()])
    gender = HiddenField('Gender', validators=[DataRequired()])
    occupation = HiddenField('Occupation', validators=[DataRequired()])
    trading = HiddenField('Trading name', validators=[DataRequired()])





