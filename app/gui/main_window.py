import os
import sys
from pathlib import Path

from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QTableWidget, QVBoxLayout, QHeaderView, QTableWidgetItem, \
    QPushButton, QHBoxLayout, QMessageBox
from PyQt5 import uic

from app.db.models.maps import Maps
from app.db.models.matches import Matches
from app.db.models.players import Players
from app.db.models.teams import Teams
from app.gui.pages import MatchesPage, PlayersPage, TeamsPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Полный путь к UI-файлу
        ui_path = Path(__file__).parent / 'ui' / 'MainWindow.ui'
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))

        # Загружаем UI
        uic.loadUi(ui_path, self)

        self._init_pages()
        self._init_navigation()

    def _init_pages(self):
        self.matches_page = MatchesPage()
        self.players_page = PlayersPage()
        self.teams_page = TeamsPage()

        self.stackedWidget.addWidget(self.matches_page)
        self.stackedWidget.addWidget(self.players_page)
        self.stackedWidget.addWidget(self.teams_page)

    def _init_navigation(self):
        self.pushButton_matches.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.matches_page))
        self.pushButton_players.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.players_page))
        self.pushButton_teams.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.teams_page))


class AdminWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('CS:GO Match Tracker - Admin Panel')
        self.setGeometry(100, 100, 800, 600)
