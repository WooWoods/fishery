"""init migration

Revision ID: 22d77e6b3f68
Revises: 
Create Date: 2017-10-22 13:47:57.679744

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22d77e6b3f68'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fishes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fishname', sa.Text(), nullable=True),
    sa.Column('latin_name', sa.Text(), nullable=True),
    sa.Column('info', sa.Text(), nullable=True),
    sa.Column('pic_url', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('fishes')
    # ### end Alembic commands ###
