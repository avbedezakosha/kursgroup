from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy
from PyQt5.QtCore import Qt
from app.db.models.matches import Matches
from app.db.models.players import Players
from app.db.models.teams import Teams
from app.gui.cards import MatchCard, PlayerCard, TeamCard, CardList
from app.gui.detail import MatchDetailWindow, PlayerDetailWindow, TeamDetailWindow


class ListPageTemplate(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()
        self._data_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Добавляем политику размеров

    def _init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы

        self._data_list = CardList()
        self.layout.addWidget(self._data_list)


class MatchesPage(ListPageTemplate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_matches()

    def load_matches(self):
        self._data_list.clear()
        matches = Matches.all()
        for match in matches:
            card = MatchCard(match)
            card.clicked.connect(self.show_match_details)
            self._data_list.add_card(card)

    def show_match_details(self, match_id):
        dialog = MatchDetailWindow(match_id, self)
        dialog.exec_()

class PlayersPage(ListPageTemplate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_players()

    def load_players(self):
        self._data_list.clear()
        players = Players.all()
        for player in players:
            card = PlayerCard(player)
            card.clicked.connect(self.show_player_details)  # Добавьте сигнал
            self._data_list.add_card(card)

    def show_player_details(self, player_id):
        dialog = PlayerDetailWindow(player_id, self)
        dialog.exec_()

class TeamsPage(ListPageTemplate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.load_teams()

    def load_teams(self):
        self._data_list.clear()
        teams = Teams.all()
        for team in teams:
            card = TeamCard(team)
            card.clicked.connect(self.show_team_details)  # Добавьте сигнал
            self._data_list.add_card(card)

    def show_team_details(self, team_id):
        dialog = TeamDetailWindow(team_id, self)
        dialog.exec_()
