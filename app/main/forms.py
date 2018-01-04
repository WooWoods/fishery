# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Required, Length


class SearchForm(FlaskForm):
    fishname = StringField(validators=[Required()])
    submit = SubmitField(u'搜索')


class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

class NewRecordForm(FlaskForm):
    fishname = StringField(validators=[Required()])
    introduction = TextAreaField('introduction')
    latin_name = StringField('latin name')
    other_names = StringField('other names')
    order = StringField('order')
    family = StringField('family')
    genus = StringField('genus')
    body_feature = TextAreaField('body feature')
    life_habit = TextAreaField('life habit')
    distribution = TextAreaField('distribution')
    level = TextAreaField('level')
    submit = SubmitField('submit')

