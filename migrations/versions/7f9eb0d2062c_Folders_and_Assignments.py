"""Folders and Assignments

Revision ID: 7f9eb0d2062c
Revises: e4d34b0c5068
Create Date: 2018-07-09 18:15:14.197282

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f9eb0d2062c'
down_revision = 'e4d34b0c5068'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('assignment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('date_issued', sa.DateTime(), nullable=True),
    sa.Column('due_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('assignment', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_assignment_date_issued'), ['date_issued'], unique=False)
        batch_op.create_index(batch_op.f('ix_assignment_due_date'), ['due_date'], unique=False)
        batch_op.create_index(batch_op.f('ix_assignment_title'), ['title'], unique=False)

    op.create_table('folders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('base_id', sa.String(length=128), nullable=True),
    sa.Column('notes_id', sa.String(length=128), nullable=True),
    sa.Column('assignments_id', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('folders')
    with op.batch_alter_table('assignment', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_assignment_title'))
        batch_op.drop_index(batch_op.f('ix_assignment_due_date'))
        batch_op.drop_index(batch_op.f('ix_assignment_date_issued'))

    op.drop_table('assignment')
    # ### end Alembic commands ###
