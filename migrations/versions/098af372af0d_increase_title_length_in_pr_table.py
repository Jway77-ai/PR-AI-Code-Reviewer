"""Increase title length in PR table

Revision ID: 098af372af0d
Revises: 277f376f7684
Create Date: 2024-09-17 21:04:56.867438

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '098af372af0d'
down_revision = '277f376f7684'
branch_labels = None
depends_on = None


def upgrade():
    # Increase the length of the 'title' column in the 'PR' table
    with op.batch_alter_table('PR', schema=None) as batch_op:
        batch_op.alter_column('title',
                              existing_type=sa.String(length=200),
                              type_=sa.String(length=500),  # Adjust the new length as needed
                              existing_nullable=False)

def downgrade():
    # Revert the length of the 'title' column if downgrading
    with op.batch_alter_table('PR', schema=None) as batch_op:
        batch_op.alter_column('title',
                              existing_type=sa.String(length=500),
                              type_=sa.String(length=200),
                              existing_nullable=False)