"""empty message

Revision ID: 1f89ced8ee46
Revises: 
Create Date: 2024-12-18 18:41:43.060068

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1f89ced8ee46'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.alter_column('event_description',
               existing_type=sa.TEXT(),
               type_=sa.String(length=2000),
               existing_nullable=False)
        batch_op.alter_column('event_date',
               existing_type=sa.DATE(),
               type_=sa.DateTime(),
               existing_nullable=False)
        batch_op.alter_column(
              'event_start_time',
              existing_type=postgresql.TIME(),
              type_=sa.DateTime(),
              existing_nullable=False,
              postgresql_using="CAST(CURRENT_DATE AS timestamp) + event_start_time")
        batch_op.alter_column('event_end_time',
               existing_type=postgresql.TIME(),
               type_=sa.DateTime(),
               existing_nullable=True,
               postgresql_using="CAST(CURRENT_DATE AS timestamp) + event_end_time")
        batch_op.alter_column('event_price',
               existing_type=sa.NUMERIC(precision=10, scale=2),
               type_=sa.Integer(),
               existing_nullable=False)
        batch_op.drop_constraint('events_new_event_admin_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'admins', ['event_admin_id'], ['id'])

    with op.batch_alter_table('tickets', schema=None) as batch_op:
        batch_op.drop_constraint('tickets_event_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'events', ['event_id'], ['id'])

def downgrade():
    with op.batch_alter_table('tickets', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('tickets_event_id_fkey', 'events', ['event_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('events_new_event_admin_id_fkey', 'admins', ['event_admin_id'], ['id'], ondelete='CASCADE')
        batch_op.alter_column('event_price',
               existing_type=sa.Integer(),
               type_=sa.NUMERIC(precision=10, scale=2),
               existing_nullable=False)
        batch_op.alter_column('event_end_time',
               existing_type=sa.DateTime(),
               type_=postgresql.TIME(),
               existing_nullable=True)
        batch_op.alter_column('event_start_time',
               existing_type=sa.DateTime(),
               type_=postgresql.TIME(),
               existing_nullable=False)
        batch_op.alter_column('event_date',
               existing_type=sa.DateTime(),
               type_=sa.DATE(),
               existing_nullable=False)
        batch_op.alter_column('event_description',
               existing_type=sa.String(length=2000),
               type_=sa.TEXT(),
               existing_nullable=False)

    # ### end Alembic commands ###
