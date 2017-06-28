"""empty message

Revision ID: 828d8fd02f13
Revises: 4e8fecae7b9c
Create Date: 2017-06-27 14:42:43.358770

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '828d8fd02f13'
down_revision = '4e8fecae7b9c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('avatar_hash', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar_hash')
    # ### end Alembic commands ###
