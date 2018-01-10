"""init migration

Revision ID: c3d7d882fb41
Revises: 
Create Date: 2018-01-08 19:55:08.071694

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3d7d882fb41'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('exercise',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.Text(), nullable=True),
    sa.Column('answered', sa.Boolean(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_index(op.f('ix_exercise_timestamp'), 'exercise', ['timestamp'], unique=False)
    op.create_table('fishes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fishname', sa.String(length=64), nullable=True),
    sa.Column('latin_name', sa.String(length=64), nullable=True),
    sa.Column('other_names', sa.Text(), nullable=True),
    sa.Column('order', sa.String(length=64), nullable=True),
    sa.Column('family', sa.String(length=64), nullable=True),
    sa.Column('genus', sa.String(length=64), nullable=True),
    sa.Column('introduction', sa.Text(), nullable=True),
    sa.Column('feature', sa.Text(), nullable=True),
    sa.Column('habit', sa.Text(), nullable=True),
    sa.Column('distribution', sa.Text(), nullable=True),
    sa.Column('level', sa.Text(), nullable=True),
    sa.Column('pic_url', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('pic_url')
    )
    op.create_index(op.f('ix_fishes_fishname'), 'fishes', ['fishname'], unique=True)
    op.create_index(op.f('ix_fishes_latin_name'), 'fishes', ['latin_name'], unique=True)
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('default', sa.Boolean(), nullable=True),
    sa.Column('permissions', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_roles_default'), 'roles', ['default'], unique=False)
    op.create_index(op.f('ix_roles_name'), 'roles', ['name'], unique=True)
    op.create_table('teams',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('captain', sa.String(length=64), nullable=True),
    sa.Column('members', sa.PickleType(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_teams_captain'), 'teams', ['captain'], unique=True)
    op.create_table('teamworks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_table('exerciseTaken',
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['class_id'], ['exercise.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['users.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('exerciseTaken')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('teamworks')
    op.drop_index(op.f('ix_teams_captain'), table_name='teams')
    op.drop_table('teams')
    op.drop_index(op.f('ix_roles_name'), table_name='roles')
    op.drop_index(op.f('ix_roles_default'), table_name='roles')
    op.drop_table('roles')
    op.drop_index(op.f('ix_fishes_latin_name'), table_name='fishes')
    op.drop_index(op.f('ix_fishes_fishname'), table_name='fishes')
    op.drop_table('fishes')
    op.drop_index(op.f('ix_exercise_timestamp'), table_name='exercise')
    op.drop_table('exercise')
    # ### end Alembic commands ###