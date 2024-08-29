import json

from flask_smorest import abort

from backend.extensions import db
from backend.models import Event
from backend.models.match import MatchStatus, Match
from backend.utils import log


class MatchEventService:
    def __init__(self):
        with open("/static/rules.json") as f:
            self.rules = json.load(f)

    def process_event(self, match_id, game_type, event_type, data):
        # 1. Получение всех событий для матча
        events = (
            Event.query.filter(Event.match_id == match_id)
            .order_by(Event.timestamp.asc())
            .all()
        )

        # 2. Восстановление текущего состояния матча
        match_state = self._reconstruct_match_state(events, game_type)

        # 3. Валидация и применение нового события
        self.validate_event(match_id, game_type, event_type, data)
        match_state = self._apply_event(match_state, event_type, data)

        # 4. Проверка условий победы
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
        match_state = {}
        # Логика восстановления состояния матча по предыдущим событиям
        for event in events:
            match_state = self._apply_event(match_state, event.event_type, event.data)
        return match_state

    def _apply_event(self, match_state, event_type, data):
        # Логика применения события к состоянию матча
        # Например, обновление позиции шаров, изменение счетов и т.д.
        if event_type == "hit_ball":
            # Пример обработки события удара
            ball_number = data["ball_number"]
            match_state["balls_hit"].append(ball_number)
        elif event_type == "pocket_ball":
            ball_number = data["ball_number"]
            match_state["balls_pocketed"].append(ball_number)
        # Добавить другие типы событий...
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

        # Создание записи о победе
        # Предполагается, что есть логика для определения победителя
        winner = self._determine_winner(match_state)
        match.winner = winner

        # Обновление профилей игроков
        self._update_player_profiles(match.player1, match.player2, winner)

        # Сохранение изменений в базе данных
        db.session.commit()

    def _determine_winner(self, match_state):
        # Логика определения победителя на основе состояния матча
        # Например, если игрок 1 выиграл
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
