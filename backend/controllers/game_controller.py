import random

from backend.models import Event


class MatchService:
    def __init__(self, match, players, db_session):
        self.match = match
        self.players = players
        self.db_session = db_session
        self.current_player = None
        self.balls_selected = False  # Определяет, выбраны ли шары для каждого игрока
        self.player_balls = {
            player.id: None for player in players
        }  # Связь игрока с типом шаров (например, четные или нечетные)

    def draw_lots(self):
        """Проведение жеребьёвки."""
        random.shuffle(self.players)
        self.current_player = self.players[0]
        print(f"Игрок {self.current_player.name} ходит первым.")

    def select_balls(self, ball_pocketed):
        """Фаза выбора шаров."""
        if not self.balls_selected:
            if ball_pocketed % 2 == 0:
                self.player_balls[self.current_player.id] = "even"
                self.player_balls[self.players[1].id] = "odd"
            else:
                self.player_balls[self.current_player.id] = "odd"
                self.player_balls[self.players[1].id] = "even"
            self.balls_selected = True
            print(
                f"Игрок {self.current_player.name} забивает {self.player_balls[self.current_player.id]} шары."
            )

    def pocket_ball(self, ball_number, pocket_number):
        """Контроль забития шара в лузу."""
        if not self.balls_selected:
            self.select_balls(ball_number)

        if self.is_correct_ball(ball_number):
            print(
                f"Игрок {self.current_player.name} забил правильный шар {ball_number} в лузу {pocket_number}."
            )
            self.record_action(ball_number, pocket_number, success=True)
            if not self.check_victory_condition():
                return  # Игрок продолжает ход
        else:
            print(
                f"Игрок {self.current_player.name} промахнулся или забил неправильный шар {ball_number}."
            )
            self.record_action(ball_number, pocket_number, success=False)
            self.switch_player()

    def is_correct_ball(self, ball_number):
        """Проверка, правильный ли шар был забит."""
        player_ball_type = self.player_balls[self.current_player.id]
        if player_ball_type == "even" and ball_number % 2 == 0:
            return True
        elif player_ball_type == "odd" and ball_number % 2 != 0:
            return True
        return False

    def switch_player(self):
        """Переключение на следующего игрока."""
        self.current_player = (
            self.players[1]
            if self.current_player == self.players[0]
            else self.players[0]
        )
        print(f"Теперь ходит игрок {self.current_player.name}.")

    def record_action(self, ball_number, pocket_number, success):
        """Запись каждого хода в базу данных."""
        action_data = {
            "match_id": self.match.current_match.id,
            "player_id": self.current_player.id,
            "event_type": "pocket_ball",
            "details": f"Ball {ball_number} pocketed in pocket {pocket_number}, Success: {success}",
        }
        action = Event(**action_data)
        self.db_session.add(action)
        self.db_session.commit()
        print(f"Записано действие: {action.details}")

    def check_victory_condition(self):
        """Проверка условия победы (например, все шары одного типа забиты)."""
        # Пример простого условия победы
        player_ball_type = self.player_balls[self.current_player.id]
        if all(
            self.is_correct_ball(ball_number) for ball_number in self.remaining_balls()
        ):
            print(f"Игрок {self.current_player.name} выиграл!")
            self.match.status = "completed"
            self.match.winner_id = self.current_player.id
            self.db_session.commit()
            return True
        return False

    def remaining_balls(self):
        """Возвращает список оставшихся шаров."""
        # Заглушка: нужно получить реальные данные из базы данных или другого источника
        return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Примерный список шаров
