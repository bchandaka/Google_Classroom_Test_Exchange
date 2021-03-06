"""empty message

Revision ID: a83d390fb451
Revises: 8246c709d9aa
Create Date: 2018-06-25 15:42:14.262079

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a83d390fb451'
down_revision = '8246c709d9aa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roster',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.String(length=64), nullable=True),
    sa.Column('tournament', sa.String(length=64), nullable=True),
    sa.Column('event', sa.String(length=64), nullable=True),
    sa.Column('user1_id', sa.Integer(), nullable=True),
    sa.Column('user2_id', sa.Integer(), nullable=True),
    sa.Column('user3_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user1_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user2_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user3_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_roster_date'), 'roster', ['date'], unique=False)
    op.create_index(op.f('ix_roster_event'), 'roster', ['event'], unique=False)
    op.create_index(op.f('ix_roster_tournament'), 'roster', ['tournament'], unique=False)
    op.drop_index('ix_user_username', table_name='user')
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.create_index('ix_user_username', 'user', ['username'], unique=False)
    op.drop_index(op.f('ix_roster_tournament'), table_name='roster')
    op.drop_index(op.f('ix_roster_event'), table_name='roster')
    op.drop_index(op.f('ix_roster_date'), table_name='roster')
    op.drop_table('roster')
    # ### end Alembic commands ###
