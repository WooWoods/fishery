# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class NameForm(FlaskForm):
    fishname = StringField(validators=[Required()])
    submit = SubmitField(u'搜索')
