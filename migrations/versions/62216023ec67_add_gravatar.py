"""add gravatar

Revision ID: 62216023ec67
Revises: 
Create Date: 2018-03-04 21:23:36.404494

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62216023ec67'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_exercise_timestamp'), 'exercise', ['timestamp'], unique=False)
    op.add_column('users', sa.Column('avatar_hash', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar_hash')
    op.drop_index(op.f('ix_exercise_timestamp'), table_name='exercise')
    # ### end Alembic commands ###
