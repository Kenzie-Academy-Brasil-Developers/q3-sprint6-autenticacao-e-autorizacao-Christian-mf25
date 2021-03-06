"""Create table users

Revision ID: 943dda28aa9a
Revises: 
Create Date: 2022-02-26 17:20:30.804926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '943dda28aa9a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=127), nullable=False),
    sa.Column('last_name', sa.String(length=511), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password_hash', sa.String(length=511), nullable=False),
    sa.Column('api_key', sa.String(length=511), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
