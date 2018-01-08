# -*- coding: utf-8 -*-
from flask import render_template, session, redirect, url_for, current_app, jsonify
from flask_login import login_required, current_user
from .. import db
from ..models import Fishes
from . import main
from .forms import SearchForm, NewRecordForm


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
            fishdata_to_front = fishdata.to_frontend()
        return render_template('searched_record.html', form=form, fishdata=fishdata_to_front)
    return render_template('index_base.html', form=form)

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

@main.route('/edit-record/<fishname>', methods=['GET', 'POST'])
@login_required
def edit_record(fishname):
    form = NewRecordForm()
    fishdata = Fishes.query.filter_by(fishname=fishname).first()
    if form.validate_on_submit():
        curr_fish = Fishes(fishname=form.fishname.data,
                           latin_name = form.latin_name.data,
                           other_names = form.other_names.data,
                           order = form.order.data,
                           family = form.family.data,
                           genus = form.genus.data,
                           introdut = form.introdution.data,
                           feature = form.body_feature.data,
                           habit = form.life_habit.data,
                           distribution = form.distribution.data,
                           level = form.level.data,
                           )
        db.session.add(curr_fish)
        db.commit()
        flash('Record update successfully.')
        return render_template('new_record.html', form=form)
    form.fishname.data = fishdata.fishname
    form.latin_name.data = fishdata.latin_name
    form.other_names.data = fishdata.other_names
    form.order.data = fishdata.order
    form.family.data = fishdata.family
    form.genus.data = fishdata.genus
    form.introdution.data = fishdata.introdution
    form.body_feature.data = fishdata.feature
    form.life_habit.data = fishdata.habit
    form.distribution.data = fishdata.distribution
    form.level.data = fishdata.level
    return render_template('new_record.html', form=form)

    
@main.route('/new-record', methods=['GET', 'POST'])
@login_required
def new_record():
    form = NewRecordForm()
    if form.validate_on_submit():
        newfish = Fishes(fishname=form.fishname.data,
                         latin_name = form.latin_name.data,
                         other_names = form.other_names.data,
                         order = form.order.data,
                         family = form.family.data,
                         genus = form.genus.data,
                         introdut = form.introdution.data,
                         feature = form.body_feature.data,
                         habit = form.life_habit.data,
                         distribution = form.distribution.data,
                         level = form.level.data,
                         )
        db.session.add(newfish)
        flash('New record added successfully')
        return redirect(url_for('.user_profile'))
    return render_template('add_record.html', form=form)

@main.route('/bbs')
def bbs():
    return

@main.route('/user/<username>')
def user_profile(username):
    return

@main.route('/about')
def about():
    form = SearchForm()
    return render_template('aboutus.html', form=form)

@main.route('/exercises')
def exercises():
    return

@main.route('/contact')
def contact():
    return
