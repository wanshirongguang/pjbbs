"""empty message

Revision ID: b3a8ed604978
Revises: 5335af8f4e79
Create Date: 2018-09-25 08:44:00.959204

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b3a8ed604978'
down_revision = '5335af8f4e79'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('_password', sa.String(length=50), nullable=False))
    op.drop_column('user', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', mysql.VARCHAR(length=50), nullable=False))
    op.drop_column('user', '_password')
    # ### end Alembic commands ###
