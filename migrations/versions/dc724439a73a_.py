"""empty message

Revision ID: dc724439a73a
Revises: 034efdba1053
Create Date: 2018-09-28 21:25:21.518542

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc724439a73a'
down_revision = '034efdba1053'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('board', sa.Column('postnum', sa.String(length=200), nullable=False))
    op.create_unique_constraint(None, 'board', ['postnum'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'board', type_='unique')
    op.drop_column('board', 'postnum')
    # ### end Alembic commands ###
