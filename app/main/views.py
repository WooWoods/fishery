# -*- coding: utf-8 -*-
from flask import render_template, session, redirect, url_for, current_app, jsonify
from .. import db
from ..models import Fishes
from . import main
from .forms import NameForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        fishdata = Fishes.query.filter_by(fishname=form.fishname.data).first()
        if fishdata is None:
            session['found'] = False
            session['pageinfo'] = u"没有你要查找的物种"
        else:
            session['found'] = True
            pageinfo = dict(fishname=fishdata.fishname, 
                            latin_name=fishdata.latin_name, 
                            info=fishdata.info, 
                            pic_url=fishdata.pic_url)
            session['pageinfo'] = pageinfo
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, found=session.get('found', False), pageinfo=session.get('pageinfo',''))
