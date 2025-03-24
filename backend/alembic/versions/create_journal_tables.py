"""create journal tables

Revision ID: create_journal_tables
Revises: 
Create Date: 2025-03-11 18:49:43.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = 'create_journal_tables'
down_revision = None
branch_labels = None
depends_on = None

def has_table(table_name):
    bind = op.get_bind()
    inspector = inspect(bind)
    return table_name in inspector.get_table_names()

def upgrade():
    # Create users table if it doesn't exist
    if not has_table('users'):
        op.create_table(
            'users',
            sa.Column('id', sa.String(), nullable=False),
            sa.Column('email', sa.String(), nullable=False),
            sa.Column('hashed_password', sa.String(), nullable=False),
            sa.Column('full_name', sa.String(), nullable=True),
            sa.Column('createdAt', sa.DateTime(), nullable=False),
            sa.Column('updatedAt', sa.DateTime(), nullable=False),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # Create journals table if it doesn't exist
    if not has_table('journals'):
        op.create_table(
            'journals',
            sa.Column('id', sa.String(), nullable=False),
            sa.Column('title', sa.String(), nullable=False),
            sa.Column('content', sa.Text(), nullable=False),
            sa.Column('tags', sa.Text(), nullable=False, server_default='[]'),
            sa.Column('createdAt', sa.DateTime(), nullable=False),
            sa.Column('updatedAt', sa.DateTime(), nullable=False),
            sa.Column('user_id', sa.String(), nullable=False),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
            sa.PrimaryKeyConstraint('id')
        )

def downgrade():
    if has_table('journals'):
        op.drop_table('journals')
    if has_table('users'):
        op.drop_index(op.f('ix_users_email'), table_name='users')
        op.drop_table('users')
