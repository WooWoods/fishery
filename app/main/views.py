# -*- coding: utf-8 -*-
from flask import render_template, session, redirect, url_for, current_app, jsonify, flash, request
from flask_login import login_required, current_user
from .. import db
from ..models import Fishes, User, Post, Permission, Comment
from . import main
from .forms import SearchForm, NewRecordForm, EditProfileForm, PostForm, CommentForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        fishdata = Fishes.query.filter_by(fishname=form.fishname.data).first()
        if fishdata is None:
            flash(u'没有你查找的物种')
            return redirect(url_for('.index'))
            #return render_template('index_base.html', form=form)
        else:
            session['found'] = True
            fishdata_to_front = fishdata.to_frontend()
            return render_template('searched_record.html', form=form, fishdata=fishdata_to_front)
    #else:
    #    print form.errors
    return render_template('index_base.html', form=form)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.username
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
        return redirect('.user_profile')
    return render_template('add_record.html', form=form)

@main.route('/bbs', methods=['GET', 'POST'])
def bbs():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(body=form.body.data,
                author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.bbs'))
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
            page, per_page=current_app.config['POSTS_PER_PAGE'],
            error_out=False
            )
    posts = pagination.items
    # posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('bbs.html', form=form, posts=posts,pagination=pagination)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_profile.html', user=user)

@main.route('/user-posts/<username>')
def user_posts(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user_posts.html', posts=posts)

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

@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                post=post,
                author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('main.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
                current_app.config['COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
            page, per_page=current_app.config['COMMENTS_PER_PAGE'],
            error_out=False
            )
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
            comments=comments, pagination=pagination)

    # return render_template('post.html', posts=[post])

