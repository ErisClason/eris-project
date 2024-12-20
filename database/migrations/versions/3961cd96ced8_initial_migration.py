"""Initial migration

Revision ID: 3961cd96ced8
Revises: None
Create Date: 2024-11-28 15:50:50.731135

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '3961cd96ced8'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('some_model',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_some_model_id'), 'some_model', ['id'], unique=False)
    op.create_index(op.f('ix_some_model_name'), 'some_model', ['name'], unique=False)
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_some_model_name'), table_name='some_model')
    op.drop_index(op.f('ix_some_model_id'), table_name='some_model')
    op.drop_table('some_model')
    # ### end Alembic commands ###
