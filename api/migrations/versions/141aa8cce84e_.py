"""empty message

Revision ID: 141aa8cce84e
Revises: 
Create Date: 2024-09-12 22:45:52.487678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '141aa8cce84e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('PR',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pr_id', sa.String(length=200), nullable=False),
    sa.Column('sourceBranchName', sa.String(length=200), nullable=False),
    sa.Column('targetBranchName', sa.String(length=200), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('feedback', sa.Text(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('PR')
    # ### end Alembic commands ###
