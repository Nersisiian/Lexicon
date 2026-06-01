"""initial audit table

Revision ID: 001
Create Date: 2024-09-01
"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None

def upgrade():
    op.create_table(
        'audit_events',
        sa.Column('event_id', sa.UUID(), primary_key=True),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('trace_id', sa.String(), nullable=False),
        sa.Column('span_id', sa.String(), nullable=False),
        sa.Column('service', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('payload', sa.JSON(), nullable=False),
    )

def downgrade():
    op.drop_table('audit_events')