"""Fix show relations mapping definition

Revision ID: 137752ab0e59
Revises: ad27edec789d
Create Date: 2020-01-24 14:27:56.423983

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '137752ab0e59'
down_revision = 'ad27edec789d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('show', sa.Column('artist_id', sa.Integer(), nullable=False))
    op.add_column('show', sa.Column('venue_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'show', 'venue', ['venue_id'], ['id'])
    op.create_foreign_key(None, 'show', 'artist', ['artist_id'], ['id'])
    op.drop_column('show', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('show', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_constraint(None, 'show', type_='foreignkey')
    op.drop_constraint(None, 'show', type_='foreignkey')
    op.drop_column('show', 'venue_id')
    op.drop_column('show', 'artist_id')
    # ### end Alembic commands ###
