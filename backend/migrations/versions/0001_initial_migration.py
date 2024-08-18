"""Initial migration
Revision ID: 0001
Revises: 
Create Date: 2024-08-05 08:44:17.324597
"""
from alembic import op
import sqlalchemy as sa
import logging
from sqlalchemy.exc import OperationalError
log = logging.getLogger(__name__)
# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    print(f"Apply migration - {revision}")
    log.debug(f"Apply migration - {revision}")
    try:
        op.create_table(
            "club",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("name", sa.String(length=255), nullable=False),
            sa.Column("description", sa.Text(), nullable=True),
            sa.PrimaryKeyConstraint("id"),
        )
    except OperationalError as e:
        log.debug(f"Revision {revision} - Table exist. Original message: {e.orig}")
        print(f"Revision {revision} - Table exist. Original message: {e.orig}")
    try:
        op.create_table(
            "news",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("title", sa.String(length=255), nullable=False),
            sa.Column("body", sa.Text(), nullable=False),
            sa.Column("source_type", sa.String(length=50), nullable=False),
            sa.Column("source_id", sa.Integer(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint("id"),
        )
    except OperationalError as e:
        log.debug(f"Revision {revision} - Table exist. Original message: {e.orig}")
        print(f"Revision {revision} - Table exist. Original message: {e.orig}")
    try:
        op.create_table(
            "play_type",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("name", sa.String(length=50), nullable=False),
            sa.Column("description", sa.String(length=255), nullable=True),
            sa.PrimaryKeyConstraint("id"),
        )
    except OperationalError as e:
        log.debug(f"Revision {revision} - Table exist. Original message: {e.orig}")
        print(f"Revision {revision} - Table exist. Original message: {e.orig}")
    try:
        op.create_table(
            "role",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("name", sa.String(length=80), nullable=True),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("name"),
        )
    except OperationalError as e:
        log.debug(f"Revision {revision} - Table exist. Original message: {e.orig}")
        print(f"Revision {revision} - Table exist. Original message: {e.orig}")
    try:
        op.create_table(
            "season",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("name", sa.String(length=64), nullable=False),
            sa.Column("start_date", sa.Date(), nullable=False),
            sa.Column("end_date", sa.Date(), nullable=False),
            sa.PrimaryKeyConstraint("id"),
        )
    except OperationalError as e:
        log.debug(f"Revision {revision} - Table exist. Original message: {e.orig}")
        print(f"Revision {revision} - Table exist. Original message: {e.orig}")
    try:
        op.create_table(
            "tag",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("name", sa.String(length=50), nullable=False),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("name"),
        )
    except OperationalError as e:
        log.debug(f"Revision {revision} - Table exist. Original message: {e.orig}")
        print(f"Revision {revision} - Table exist. Original message: {e.orig}")
    try:
        op.create_table(
            "user",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("email", sa.String(), nullable=True),
            sa.Column("active", sa.Boolean(), nullable=True),
            sa.Column("password_hash", sa.String(length=255), nullable=False),
            sa.Column("salt", sa.String(length=32), nullable=False),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("email"),
        )
    except OperationalError as e:
        log.debug(f"Revision {revision} - Table exist. Original message: {e.orig}")
        print(f"Revision {revision} - Table exist. Original message: {e.orig}")
    try:
        op.create_table(
            "win_reason",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("description", sa.String(length=255), nullable=False),
            sa.PrimaryKeyConstraint("id"),
        )
    except OperationalError as e:
        log.debug(f"Revision {revision} - Table exist. Original message: {e.orig}")
        print(f"Revision {revision} - Table exist. Original message: {e.orig}")
    try:
        op.create_table(
            "news_tags",
            sa.Column("news_id", sa.Integer(), nullable=True),
            sa.Column("tag_id", sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(
                ["news_id"],
                ["news.id"],
            ),
            sa.ForeignKeyConstraint(
                ["tag_id"],
                ["tag.id"],
            ),
        )
    except OperationalError as e:
        log.debug(f"Revision {revision} - Table exist. Original message: {e.orig}")
        print(f"Revision {revision} - Table exist. Original message: {e.orig}")
    try:
        op.create_table(
            "player",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("user_id", sa.Integer(), nullable=False),
            sa.Column("played_games", sa.Integer(), nullable=False),
            sa.Column("score", sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(
                ["user_id"],
                ["user.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
        )
    except OperationalError as e:
        log.debug(f"Revision {revision} - Table exist. Original message: {e.orig}")
        print(f"Revision {revision} - Table exist. Original message: {e.orig}")
    try:
        op.create_table(
            "roles_users",
            sa.Column("user_id", sa.Integer(), nullable=True),
            sa.Column("role_id", sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(
                ["role_id"],
                ["role.id"],
            ),
            sa.ForeignKeyConstraint(
                ["user_id"],
                ["user.id"],
            ),
        )
    except OperationalError as e:
        log.debug(f"Revision {revision} - Table exist. Original message: {e.orig}")
        print(f"Revision {revision} - Table exist. Original message: {e.orig}")
    try:
        op.create_table(
            "tournament",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("name", sa.String(length=64), nullable=False),
            sa.Column("season_id", sa.Integer(), nullable=False),
            sa.Column("start_date", sa.Date(), nullable=False),
            sa.Column("end_date", sa.Date(), nullable=False),
            sa.ForeignKeyConstraint(
                ["season_id"],
                ["season.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
        )
    except OperationalError as e:
        log.debug(f"Revision {revision} - Table exist. Original message: {e.orig}")
        print(f"Revision {revision} - Table exist. Original message: {e.orig}")
    try:
        op.create_table(
            "game",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("player1_id", sa.Integer(), nullable=False),
            sa.Column("player2_id", sa.Integer(), nullable=False),
            sa.Column("score_player1", sa.Integer(), nullable=True),
            sa.Column("score_player2", sa.Integer(), nullable=True),
            sa.Column("tournament_id", sa.Integer(), nullable=True),
            sa.Column("season_id", sa.Integer(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.Column("ended_at", sa.DateTime(), nullable=True),
            sa.Column("winner_id", sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(
                ["player1_id"],
                ["player.id"],
            ),
            sa.ForeignKeyConstraint(
                ["player2_id"],
                ["player.id"],
            ),
            sa.ForeignKeyConstraint(
                ["season_id"],
                ["season.id"],
            ),
            sa.ForeignKeyConstraint(
                ["tournament_id"],
                ["tournament.id"],
            ),
            sa.ForeignKeyConstraint(
                ["winner_id"],
                ["player.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
        )
    except OperationalError as e:
        log.debug(f"Revision {revision} - Table exist. Original message: {e.orig}")
        print(f"Revision {revision} - Table exist. Original message: {e.orig}")
    try:
        op.create_table(
            "play",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("game_id", sa.Integer(), nullable=False),
            sa.Column("type_id", sa.Integer(), nullable=False),
            sa.Column("start_time", sa.DateTime(), nullable=True),
            sa.Column("end_time", sa.DateTime(), nullable=True),
            sa.Column("winner_id", sa.Integer(), nullable=True),
            sa.Column("win_reason_id", sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(
                ["game_id"],
                ["game.id"],
            ),
            sa.ForeignKeyConstraint(
                ["type_id"],
                ["play_type.id"],
            ),
            sa.ForeignKeyConstraint(
                ["win_reason_id"],
                ["win_reason.id"],
            ),
            sa.ForeignKeyConstraint(
                ["winner_id"],
                ["player.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
        )
    except OperationalError as e:
        log.debug(f"Revision {revision} - Table exist. Original message: {e.orig}")
        print(f"Revision {revision} - Table exist. Original message: {e.orig}")
    try:
        op.create_table(
            "play_event",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("play_id", sa.Integer(), nullable=False),
            sa.Column("game_id", sa.Integer(), nullable=False),
            sa.Column("player_id", sa.Integer(), nullable=False),
            sa.Column("event_type", sa.String(length=50), nullable=False),
            sa.Column("ball_number", sa.Integer(), nullable=True),
            sa.Column("event_time", sa.DateTime(), nullable=False),
            sa.Column("details", sa.String(length=255), nullable=True),
            sa.ForeignKeyConstraint(
                ["game_id"],
                ["game.id"],
            ),
            sa.ForeignKeyConstraint(
                ["play_id"],
                ["play.id"],
            ),
            sa.ForeignKeyConstraint(
                ["player_id"],
                ["player.id"],
            ),
            sa.PrimaryKeyConstraint("id"),
        )
    except OperationalError as e:
        log.debug(f"Revision {revision} - Table exist. Original message: {e.orig}")
        print(f"Revision {revision} - Table exist. Original message: {e.orig}")
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("play_event")
    op.drop_table("play")
    op.drop_table("game")
    op.drop_table("tournament")
    op.drop_table("roles_users")
    op.drop_table("player")
    op.drop_table("news_tags")
    op.drop_table("win_reason")
    op.drop_table("user")
    op.drop_table("tag")
    op.drop_table("season")
    op.drop_table("role")
    op.drop_table("play_type")
    op.drop_table("news")
    op.drop_table("club")
    # ### end Alembic commands ###
