# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Required, Length


class SearchForm(FlaskForm):
    fishname = StringField(validators=[Required()])
    submit = SubmitField(u'搜索')


class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

class NewRecordForm(FlaskForm):
    fishname = StringField('物种学名', validators=[Required()])
    latin_name = StringField('拉丁学名')
    other_names = StringField('别名')
    order = StringField('目')
    family = StringField('科')
    genus = StringField('属')
    introduction = TextAreaField('简要介绍')
    body_feature = TextAreaField('形态特征')
    life_habit = TextAreaField('生活习性')
    distribution = TextAreaField('地理分布')
    level = TextAreaField('保护级别')
    submit = SubmitField('提交')

class PostForm(FlaskForm):
    body = TextAreaField("发布新帖", validators=[Required()])
    submit = SubmitField('Submit')



