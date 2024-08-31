import json
import os

from flask_smorest import abort
from marshmallow import ValidationError

from backend.extensions import db
from backend.models import Event, EventType
from backend.models.events import FoulEventData, BallPottedEventData, HitBallEventData
from backend.models.match import MatchStatus, Match
from backend.schemas.events import (
    EventSchema,
    FoulEventSchema,
    BallPottedEventSchema,
    HitBallEventSchema,
)
from backend.utils import log


class MatchEventService:
    """
    Controller for validationg match events
    """

    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        rules_path = os.path.join(base_dir, "../static/rules.json")
        with open(rules_path) as f:
            self.rules = json.load(f)

    def get_match_log(self, match_id):
        events = (
            Event.query.filter(Event.match_id == match_id)
            .order_by(Event.timestamp.asc())
            .all()
        )
        values = EventSchema.dump(EventSchema(), events, many=True)
        return values

    def process_event(self, game_type, event_type, data, match_id, write=None):
        log.debug(f"Processing event for {match_id} - {event_type} with {data}")
        log.debug(f"process_event - {event_type} - {EventType.BALL_POTTED}")
        if event_type == "HIT_BALL":
            schema = HitBallEventSchema()
        elif event_type == "BALL_POTTED":
            schema = BallPottedEventSchema()
        elif event_type == "FOUL":
            schema = FoulEventSchema()
        else:
            abort(400, message=f"Unsupported event type: {event_type}")

        try:
            validated_data = schema.load(data, session=db.session)
        except ValidationError as err:
            abort(400, message=err.messages)

        events = (
            Event.query.filter(Event.match_id == match_id)
            .order_by(Event.timestamp.asc())
            .all()
        )
        if len(events) == 0:
            match_state = {
                "balls_hit": [],
                "balls_pocketed": [],
                "current_player_id": None,
                "turns": [],
                "fouls": [],
                "game_status": "ongoing",
                "winner_id": None,
                "last_pocketed_ball": None,
                "target_pocket": None,
                "description": None,
            }
            match_state = self._apply_event(
                match_id=match_id,
                match_state=match_state,
                event_type=event_type.upper(),
                data=validated_data,
                write=write,
                player_id=1,
            )
        else:
            match_state = self._reconstruct_match_state(events, game_type)
            match_state = self._apply_event(
                match_id=match_id,
                match_state=match_state,
                event_type=event_type,
                data=validated_data,
                write=write,
            )
        if self._check_win_condition(match_state, game_type):
            self._finalize_match(match_id, match_state)
        return match_state

    def validate_event(self, match_id, game_type, event_type, data):
        # Получение правил для конкретного типа игры и события
        game_rules = self.rules.get(game_type)
        if not game_rules:
            raise ValueError(f"No rules found for game type: {game_type}")

        event_rules = game_rules.get(event_type)
        if not event_rules:
            raise ValueError(
                f"No validation rules found for event type: {event_type} in game type: {game_type}"
            )
        log.debug("Event valid")

        # Применение каждого правила валидации
        for rule in event_rules["validations"]:
            field = rule["field"]
            if rule["type"] == "required":
                self._validate_required(field, data)
            elif rule["type"] == "range":
                self._validate_range(field, data, rule["min"], rule["max"])

        log.info(
            f"Event {event_type} for match {match_id} in game {game_type} passed validation."
        )

    def _validate_required(self, field, data):
        if field not in data:
            abort(400, message=f"Field '{field}' is required for this event.")

    def _validate_range(self, field, data, min_value, max_value):
        if field in data:
            value = data[field]
            if not (min_value <= value <= max_value):
                abort(
                    400,
                    message=f"Field '{field}' must be between {min_value} and {max_value}.",
                )
        else:
            abort(400, message=f"Field '{field}' is required for this event.")

    def _reconstruct_match_state(self, events, game_type):
        log.debug("Reconstructing match...")

        match_state = {
            "balls_hit": [],
            "balls_pocketed": [],
            "current_player_id": None,
            "turns": [],
            "fouls": [],
            "game_status": "ongoing",
            "winner_id": None,
            "last_pocketed_ball": None,
            "target_pocket": None,
            "description": None,
        }

        for event in events:
            if event.event_type == EventType.HIT_BALL:
                hit_data = HitBallEventData.query.filter_by(event_id=event.id).first()
                if hit_data:
                    match_state = self._apply_event(
                        match_id=event.match_id,
                        match_state=match_state,
                        event_type=event.event_type,
                        data={
                            "ball_number": hit_data.ball_number,
                            "force": hit_data.force,
                            "description": event.description,
                        },
                        player_id=event.player_id,
                        write=False,
                        reconstructing=True,
                    )

            elif event.event_type == EventType.BALL_POTTED:
                potted_data = BallPottedEventData.query.filter_by(
                    event_id=event.id
                ).first()
                if potted_data:
                    match_state = self._apply_event(
                        match_id=event.match_id,
                        match_state=match_state,
                        event_type=event.event_type,
                        data={
                            "ball_number": potted_data.ball_number,
                            "pocket_id": potted_data.pocket_id,
                            "description": event.description,
                        },
                        player_id=event.player_id,
                        write=False,
                        reconstructing=True,
                    )

            elif event.event_type == EventType.FOUL:
                foul_data = FoulEventData.query.filter_by(event_id=event.id).first()
                if foul_data:
                    match_state = self._apply_event(
                        match_id=event.match_id,
                        match_state=match_state,
                        event_type=event.event_type,
                        data={
                            "reason": foul_data.reason,
                            "description": event.description,
                        },
                        player_id=event.player_id,
                        write=False,
                        reconstructing=True,
                    )

        log.debug(f"Reconstructed match state: {match_state}")
        return match_state

    def _apply_event(
        self,
        match_id,
        match_state,
        event_type,
        data,
        player_id=1,
        write=False,
        reconstructing=False,
    ):
        log.debug(
            f"Applying event: {event_type} for match {match_id} with data: {data}, write={write}, player={player_id}"
        )

        if not reconstructing:
            # For new events, create a new event object and add it to the session
            new_event = Event(
                match_id=match_id,
                event_type=event_type,
                player_id=player_id,
            )
            try:
                db.session.add(new_event)
                db.session.flush()  # Ensures the new_event gets an ID before we use it in related tables
            except Exception as e:
                log.error(f"Occured exception: {e}")

            description = None  # Initialize description as None

        # Handle event types
        if event_type == EventType.HIT_BALL:
            ball_number = data.get("ball_number")
            force = data.get("force")

            if not reconstructing:
                hit_data = HitBallEventData(
                    event_id=new_event.id, ball_number=ball_number, force=force
                )
                db.session.add(hit_data)

            match_state["balls_hit"].append(ball_number)
            log.debug(f"Ball hit: {ball_number}, force: {force}")

        elif event_type == "BALL_POTTED":
            ball_number = data.ball_number
            pocket_id = data.pocket_id

            if not reconstructing:
                potted_data = BallPottedEventData(
                    event_id=new_event.id, ball_number=ball_number, pocket_id=pocket_id
                )
                db.session.add(potted_data)

                description = (
                    f"Игрок {player_id} забил шар {ball_number} в лузу {pocket_id}"
                )

            match_state["balls_pocketed"].append(ball_number)
            match_state["last_pocketed_ball"] = ball_number
            match_state["target_pocket"] = pocket_id
            log.debug(f"Ball potted: {ball_number}, pocket: {pocket_id}")

        elif event_type == EventType.FOUL:
            reason = data.get("reason")

            if not reconstructing:
                foul_data = FoulEventData(event_id=new_event.id, reason=reason)
                db.session.add(foul_data)

            match_state["fouls"].append({"player_id": player_id, "reason": reason})
            log.debug(f"Foul recorded: {reason} by player {player_id}")

        if not reconstructing and description:
            new_event.description = description

        if write and not reconstructing:
            log.debug(f"Writing new event to DB")
            try:
                db.session.commit()
                log.debug(f"Event committed to DB successfully")
            except Exception as e:
                log.error(f"Error committing event to DB: {e}")
                db.session.rollback()

        log.debug(f"Updated match_state: {match_state}")
        return match_state

    def _check_win_condition(self, match_state, game_type):
        # Логика проверки условий победы в зависимости от типа игры
        if game_type == "8ball":
            if "8" in match_state["balls_pocketed"]:
                return True
        # Добавить другие условия для других типов игр...
        return False

    def _finalize_match(self, match_id, match_state):
        # Обновление статуса матча
        match = Match.query.get(match_id)
        match.status = MatchStatus.COMPLETED
        winner = self._determine_winner(match_state)
        match.winner = winner
        self._update_player_profiles(match.player1, match.player2, winner)
        db.session.commit()

    def _determine_winner(self, match_state):
        return "player1"

    def _update_player_profiles(self, player1, player2, winner):
        # Логика обновления профилей игроков
        if winner == player1:
            player1.wins += 1
            player2.losses += 1
        else:
            player1.losses += 1
            player2.wins += 1
        db.session.commit()
