"""Add initial tags

Revision ID: 0004
Revises: 0003
Create Date: 2024-07-31 20:08:50.035347

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade():
    tags = [
        {"name": "Club News"},
        {"name": "Tournament"},
        {"name": "Game Result"},
        {"name": "Player Achievement"},
        {"name": "Announcement"},
    ]

    for tag in tags:
        op.execute(f"INSERT INTO tag (name) VALUES ('{tag['name']}')")


def downgrade():
    op.execute("DELETE FROM tag ")
