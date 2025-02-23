"""add comments count

Revision ID: a15a8564a102
Revises: d820aa5a6ad3
Create Date: 2025-02-06 01:30:38.636824

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a15a8564a102'
down_revision = 'd820aa5a6ad3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.add_column(sa.Column('comments_count', sa.Integer(), nullable=True))
        batch_op.drop_column('event_price')
        batch_op.drop_column('event_end_time')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.add_column(sa.Column('event_end_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('event_price', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.drop_column('comments_count')

    # ### end Alembic commands ###
