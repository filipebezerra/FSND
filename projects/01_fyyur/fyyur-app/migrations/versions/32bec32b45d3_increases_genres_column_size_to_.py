"""Increases genres column size to accommodate data in scenarios when user selects all options available

Revision ID: 32bec32b45d3
Revises: 302488fc993a
Create Date: 2020-02-09 21:38:46.780910

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32bec32b45d3'
down_revision = '302488fc993a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('artist', 'genres',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.String(length=200),
               existing_nullable=False)
    op.alter_column('venue', 'genres',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.String(length=200),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venue', 'genres',
               existing_type=sa.String(length=200),
               type_=sa.VARCHAR(length=120),
               existing_nullable=False)
    op.alter_column('artist', 'genres',
               existing_type=sa.String(length=200),
               type_=sa.VARCHAR(length=120),
               existing_nullable=False)
    # ### end Alembic commands ###
