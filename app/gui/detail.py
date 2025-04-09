from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLabel

from app.db.database import Database
from app.db.models.matches import Matches
from app.db.models.players import Players
from app.db.models.teams import Teams


class BaseDetailWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Детали")
        self.setMinimumSize(400, 300)
        self.layout = QVBoxLayout(self)

    def add_form_row(self, label, value):
        row = QFormLayout()
        row.addRow(QLabel(f"<b>{label}:</b>"), QLabel(str(value)))
        self.layout.addLayout(row)


# Окно для матчей
class MatchDetailWindow(BaseDetailWindow):
    def __init__(self, match_id, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.match = Matches.get_by_id(match_id)
        self._init_ui()

    def _init_ui(self):
        if not self.match:
            self.layout.addWidget(QLabel("Матч не найден"))
            return

        self.add_form_row("ID", self.match.match_id)
        self.add_form_row("Дата", self.match.match_date)
        self.add_form_row("Статус", self.match.match_status)
        self.add_form_row("Команда 1", self._get_team_name(self.match.team1_id))
        self.add_form_row("Команда 2", self._get_team_name(self.match.team2_id))

    def _get_team_name(self, team_id):
        team = Teams.get_by_id(team_id) if team_id else None
        return team.team_name if team else "Неизвестно"


# Окно для игроков
class PlayerDetailWindow(BaseDetailWindow):
    def __init__(self, player_id, parent=None):
        super().__init__(parent)
        self.player = Players.get_by_id(player_id)
        self._init_ui()

    def _init_ui(self):
        if not self.player:
            self.layout.addWidget(QLabel("Игрок не найден"))
            return

        self.add_form_row("Никнейм", self.player.nickname)
        self.add_form_row("Имя", f"{self.player.first_name} {self.player.last_name}")
        self.add_form_row("Страна", self.player.country)
        self.add_form_row("Steam ID", self.player.steam_id)


# Окно для команд
class TeamDetailWindow(BaseDetailWindow):
    def __init__(self, team_id, parent=None):
        super().__init__(parent)
        self.team = Teams.get_by_id(team_id)
        self._init_ui()

    def _init_ui(self):
        if not self.team:
            self.layout.addWidget(QLabel("Команда не найдена"))
            return

        self.add_form_row("Название", self.team.team_name)
        self.add_form_row("Капитан", self._get_captain_name())
        self.add_form_row("Количество игроков", self._get_players_count())

    def _get_captain_name(self):
        if not self.team.captain_id: return "Не назначен"
        captain = Players.get_by_id(self.team.captain_id)
        return captain.nickname if captain else "Неизвестно"

    def _get_players_count(self):
        db = Database()
        query = "SELECT COUNT(*) FROM players WHERE team_id = %s"
        result = db.fetch_query(query, (self.team.team_id,))
        return result[0][0] if result else 0
