"""Populate default values for tags

Revision ID: 0002
Revises: 0001
Create Date: 2024-08-11 19:34:38.169219

"""

from alembic import op

from backend.migrations.versions import log

# revision identifiers, used by Alembic.
revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None

tags = [
    {"name": "Club News"},
    {"name": "Tournament"},
    {"name": "Game Result"},
    {"name": "Player Achievement"},
    {"name": "Announcement"},
]


def upgrade():
    for tag in tags:
        log.info(f"{revision} - Inserted tag: {tag['name']}")
        op.execute(f"INSERT INTO tag (name) VALUES ('{tag['name']}')")


def downgrade():
    for tag in tags:
        log.info(f"{revision} - Removed tag: {tag['name']}")
        op.execute(f"DELETE FROM tag WHERE name='{tag['name']}'")
