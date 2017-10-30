# -*- coding: utf-8 -*-
from flask import render_template, session, redirect, url_for, current_app, jsonify
from flask_login import login_required, current_user
from .. import db
from ..models import Fishes
from . import main
from .forms import SearchForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        fishdata = Fishes.query.filter_by(fishname=form.fishname.data).first()
        if fishdata is None:
            session['found'] = False
            session['pageinfo'] = u"没有你要查找的物种"
        else:
            session['found'] = True
            #pageinfo = dict(fishname=fishdata.fishname, 
            #                latin_name=fishdata.latin_name, 
            #                info=fishdata.info, 
            #                pic_url=fishdata.pic_url)
            session['pageinfo'] = fishdata.json()
            print session['pageinfo']
        return redirect(url_for('.index'))
    return render_template('index_base.html', form=form)
    #return render_template('index.html', form=form, found=session.get('found', False), pageinfo=session.get('pageinfo',''))

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.location.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

@main.route('/bbs')
def bbs():
    return

@main.route('/user/<username>')
def user(username):
    return

@main.route('/about')
def about():
    return

@main.route('/exercises')
def exercises():
    return

@main.route('/contact')
def contact():
    return
