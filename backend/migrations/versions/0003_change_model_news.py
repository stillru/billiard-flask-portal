"""Change model News

Revision ID: 0003
Revises: 0002
Create Date: 2024-08-11 21:04:13.563740

"""
import logging

from alembic import op
import sqlalchemy as sa
log = logging.getLogger(__name__)


# revision identifiers, used by Alembic.
revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    log.debug(f"{revision} Drop table column source_id")
    print(f"{revision} Drop table column source_id")
    with op.batch_alter_table('news', schema=None) as batch_op:
        batch_op.drop_column('source_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    log.debug(f"{revision} - Return table column source_id to news")
    print(f"{revision} - Return table column source_id to news")
    with op.batch_alter_table('news', schema=None) as batch_op:
        batch_op.add_column(sa.Column('source_id', sa.INTEGER(), nullable=False))

    # ### end Alembic commands ###
