# -*- coding: utf-8 -*-

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from markdown import markdown
import bleach
import hashlib
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from . import db
from . import login_manager




class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    captain = db.Column(db.String(64), unique=True, index=True)
    members = db.Column(db.PickleType)

    def is_captain(self, user):
        return user.name == self.captain


class TeamWork(db.Model):
    __tablename__ = 'teamworks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)


class Exercises(db.Model):
    __tablename__ = 'exercise'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    answered = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

exerciseTaken = db.Table('exerciseTaken',
        db.Column('student_id', db.Integer, db.ForeignKey('users.id')),
        db.Column('class_id', db.Integer, db.ForeignKey('exercise.id')))


class Fishes(db.Model):
    __tablename__ = 'fishes'
    id = db.Column(db.Integer, primary_key=True)
    fishname = db.Column(db.String(64), unique=True, index=True)
    latin_name = db.Column(db.String(64), unique=True, index=True)
    other_names = db.Column(db.Text)
    order = db.Column(db.String(64))
    family = db.Column(db.String(64))
    genus = db.Column(db.String(64))
    introduction = db.Column(db.Text)
    feature = db.Column(db.Text)
    habit = db.Column(db.Text)
    distribution = db.Column(db.Text)
    level = db.Column(db.Text)
    pic_url = db.Column(db.Text)

    def to_frontend(self):
        return dict(fishname=self.fishname,
                    latin_name=self.latin_name,
                    other_names=self.other_names,
                    order=self.order,
                    family=self.family,
                    genus=self.genus,
                    introduction=self.introduction,
                    feature=self.feature,
                    habit=self.habit,
                    distribution=self.distribution,
                    level=self.level,
                    pic_url=self.pic_url,
                    )

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    about_me = db.Column(db.Text)
    avatar_hash = db.Column(db.String(32))
    username = db.Column(db.String(64), unique=True)
    student_id = db.Column(db.Integer, nullable=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    exercises = db.relationship('Exercises',
                                secondary=exerciseTaken,
                                backref=db.backref('users', lazy='dynamic'),
                                lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FISHERY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            self.role = Role.query.filter_by(default=True).first()

        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = self.gravatar_hash()

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                    username=forgery_py.internet.user_name(True),
                    password=forgery_py.lorem_ipsum.word(),
                    confirmed=True,
                    about_me=forgery_py.lorem_ipsum.sentence())
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self, size=100, default='identicon', rating='g'):
        url = 'https://secure.gravatar.com/avatar'
        hash = self.avatar_hash or self.gravatar_hash()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
                url=url, hash=hash, size=size, default=default, rating=rating
                )

    @property
    def password(self):
        raise AttributeError('password is not readable attribue')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def can(self, permissions):
        return self.role is not None and \
                (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def __repr__(self):
        return '<User %r>' % self.username

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
                'Student': (Permission.FOLLOW |
                            Permission.COMMENT |
                            Permission.WRITE_ARTICLES, True),
                'Teacher': (Permission.FOLLOW |
                            Permission.COMMENT |
                            Permission.WRITE_ARTICLES |
                            Permission.MODERATE_COMMENTS, False),
                'Administrator': (0xff, False)
                }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name

class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80

class AnonymousUser(AnonymousUserMixin):
    def can(slef, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            p = Post(body=forgery_py.lorem_ipsum.sentences(randint(1,3)),
                    timestamp=forgery_py.date.date(True),
                    author=u)
            db.session.add(p)
            db.session.commit()






