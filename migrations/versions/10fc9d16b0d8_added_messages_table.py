"""added messages table

Revision ID: 10fc9d16b0d8
Revises: 8f3ddf674b19
Create Date: 2022-07-15 14:28:03.883246

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10fc9d16b0d8'
down_revision = '8f3ddf674b19'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('chat', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['chat'], ['chats.id'], name='fk_messages_chats_id_chat'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messages')
    # ### end Alembic commands ###
