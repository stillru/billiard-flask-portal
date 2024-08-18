"""Populate default values for tags

Revision ID: 0002
Revises: 0001
Create Date: 2024-08-11 19:34:38.169219

"""
import logging

from alembic import op
import sqlalchemy as sa

log = logging.getLogger(__name__)

# revision identifiers, used by Alembic.
revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None

tags = [
    {"name": "Club News"},
    {"name": "Tournament"},
    {"name": "Game Result"},
    {"name": "Player Achievement"},
    {"name": "Announcement"}
]


def upgrade():
    for tag in tags:
        print(f"{revision} - Inserted tag: {tag['name']}")
        log.debug(f"{revision} - Inserted tag: {tag['name']}")
        op.execute(
            f"INSERT INTO tag (name) VALUES ('{tag['name']}')"
        )


def downgrade():
    for tag in tags:
        print(f"{revision} - Removed tag: {tag['name']}")
        log.debug(f"{revision} - Removed tag: {tag['name']}")
        op.execute(
            f"DELETE FROM tag WHERE name='{tag['name']}'"
        )
