"""empty message

Revision ID: 034efdba1053
Revises: d1e3c0610aac
Create Date: 2018-09-28 21:24:54.373990

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '034efdba1053'
down_revision = 'd1e3c0610aac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('board',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('boardname', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('board')
    # ### end Alembic commands ###
