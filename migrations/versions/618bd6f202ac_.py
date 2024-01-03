"""empty message

Revision ID: 618bd6f202ac
Revises: 
Create Date: 2023-12-20 21:47:34.668645

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '618bd6f202ac'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('population', sa.Integer(), nullable=False),
    sa.Column('terrain', sa.String(length=50), nullable=False),
    sa.Column('climate', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('vehicles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('model', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('favorite_planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('planet_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['planet_id'], ['planets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorite_vehicles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vehicle_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['vehicle_id'], ['vehicles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('height', sa.Float(), nullable=False),
    sa.Column('mass', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('planet_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['planet_id'], ['planets.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('favorite_people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('people_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['people_id'], ['people.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vehicles_pilots',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('people_id', sa.Integer(), nullable=True),
    sa.Column('vehicle_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['people_id'], ['people.id'], ),
    sa.ForeignKeyConstraint(['vehicle_id'], ['vehicles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vehicles_pilots')
    op.drop_table('favorite_people')
    op.drop_table('people')
    op.drop_table('favorite_vehicles')
    op.drop_table('favorite_planets')
    op.drop_table('vehicles')
    op.drop_table('planets')
    # ### end Alembic commands ###
