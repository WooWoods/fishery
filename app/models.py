# -*- coding: utf-8 -*-
from . import db


class Fishes(db.Model):
    __tablename__ = 'fishes'
    id = db.Column(db.Integer, primary_key=True)
    fishname = db.Column(db.Text)
    latin_name = db.Column(db.Text)
    info = db.Column(db.Text)
    pic_url = db.Column(db.Text)
