"""empty message

Revision ID: e1827e2a7c35
Revises: 5180de9d8814
Create Date: 2018-06-25 21:48:02.227432

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1827e2a7c35'
down_revision = '5180de9d8814'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.String(length=64), nullable=True),
    sa.Column('tournament', sa.String(length=64), nullable=True),
    sa.Column('team', sa.String(length=64), nullable=True),
    sa.Column('event_name', sa.String(length=64), nullable=True),
    sa.Column('user1_id', sa.Integer(), nullable=True),
    sa.Column('user2_id', sa.Integer(), nullable=True),
    sa.Column('user3_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user1_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user2_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user3_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_event_date'), ['date'], unique=False)
        batch_op.create_index(batch_op.f('ix_event_event_name'), ['event_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_event_team'), ['team'], unique=False)
        batch_op.create_index(batch_op.f('ix_event_tournament'), ['tournament'], unique=False)

    with op.batch_alter_table('roster', schema=None) as batch_op:
        batch_op.drop_index('ix_roster_date')
        batch_op.drop_index('ix_roster_event')
        batch_op.drop_index('ix_roster_team')
        batch_op.drop_index('ix_roster_tournament')

    op.drop_table('roster')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roster',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('date', sa.VARCHAR(length=64), nullable=True),
    sa.Column('tournament', sa.VARCHAR(length=64), nullable=True),
    sa.Column('event', sa.VARCHAR(length=64), nullable=True),
    sa.Column('user1_id', sa.INTEGER(), nullable=True),
    sa.Column('user2_id', sa.INTEGER(), nullable=True),
    sa.Column('user3_id', sa.INTEGER(), nullable=False),
    sa.Column('team', sa.VARCHAR(length=64), nullable=True),
    sa.ForeignKeyConstraint(['user1_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user2_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['user3_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('roster', schema=None) as batch_op:
        batch_op.create_index('ix_roster_tournament', ['tournament'], unique=False)
        batch_op.create_index('ix_roster_team', ['team'], unique=False)
        batch_op.create_index('ix_roster_event', ['event'], unique=False)
        batch_op.create_index('ix_roster_date', ['date'], unique=False)

    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_event_tournament'))
        batch_op.drop_index(batch_op.f('ix_event_team'))
        batch_op.drop_index(batch_op.f('ix_event_event_name'))
        batch_op.drop_index(batch_op.f('ix_event_date'))

    op.drop_table('event')
    # ### end Alembic commands ###
