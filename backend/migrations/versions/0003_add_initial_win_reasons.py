"""Add initial win reasons

Revision ID: 0003
Revises: 0002
Create Date: 2024-07-31 20:04:07.791700

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade():
    # Insert initial win reasons
    op.execute(
        sa.text(
            "INSERT INTO win_reason (description) VALUES "
            "('Player potted the 8 ball in the correct pocket'), "
            "('Opponent potted the 8 ball in the wrong pocket'), "
            "('Player potted all their balls'), "
            "('Opponent fouled multiple times')"
        )
    )


def downgrade():
    op.execute(
        "DELETE FROM winreason WHERE description IN "
        "('Player potted the 8 ball in the correct pocket', "
        "'Opponent potted the 8 ball in the wrong pocket', "
        "'Player potted all their balls', "
        "'Opponent fouled multiple times')"
    )
