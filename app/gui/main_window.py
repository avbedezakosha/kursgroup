# -*- coding: utf-8 -*-
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QByteArray, Qt
from PyQt5.QtGui import QPixmap, QIcon

from app.db.models.matches import Matches
from app.db.models.players import Players
from app.db.models.teams import Teams
from app.db.models.current_lineups import CurrentLineups
from app.db.models.match_lineups import MatchLineups
from app.db.models.maps import Maps
from app.gui.myWidgets import ClickableLabel, PlayerWidget, VersusWidget, set_widget_image

# Загрузка данных
all_teams = Teams.all()
all_matches = Matches.all()
all_players = Players.all()
all_team_lineups = CurrentLineups.all()
all_match_lineups = MatchLineups.all()
all_maps = Maps.all()


class MainWindowUI:
    @staticmethod
    def split_first_last_name(player):
        first_last_name = player.first_last_name.split()
        first_name = first_last_name[0]
        last_name = 'Отсутствует'
        if len(first_last_name) < 2:
            return first_name, last_name, f'"{player.nickname}" {first_last_name[0]}'
        else:
            last_name = first_last_name[1]
            return first_name, last_name, f'{first_last_name[1]} "{player.nickname}" {first_last_name[0]}'

    def setup_ui(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.resize(1178, 663)
        main_window.setWindowTitle('GameTracker')
        main_window.setWindowIcon(QIcon('app/gui/images/logo.jpg'))

        # Создание центрального виджета
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")

        # Настройка цветовой палитры и стилей
        self.setup_palette_and_styles(main_window)

        # Основной макет
        self.main_layout = QtWidgets.QGridLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Создание боковой панели
        self.setup_sidebar()

        # Создание основного контента
        self.setup_main_content()

        # Добавление виджетов в основной макет
        self.main_layout.addWidget(self.sidebar_frame, 0, 0, 1, 1)
        self.main_layout.addWidget(self.main_content_frame, 0, 1, 1, 1)

        main_window.setCentralWidget(self.central_widget)

        # Настройка соединений
        self.setup_connections()

        # Установка начальной страницы
        self.stacked_widget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def setup_palette_and_styles(self, window):
        """Настройка цветовой палитры и стилей для главного окна"""

        with open('app/gui/ui/styles/main.qss', "r") as f:
            stylesheet = f.read()
            self.central_widget.setStyleSheet(stylesheet)

        # palette = QtGui.QPalette()
        # palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 127))
        # palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(255, 255, 255))
        # window.setPalette(palette)

        font = QtGui.QFont()
        font.setFamily("Verdana")
        window.setFont(font)

    def setup_sidebar(self):
        """Настройка боковой панели"""
        self.sidebar_frame = QtWidgets.QFrame()
        self.sidebar_frame.setMinimumWidth(300)
        self.sidebar_frame.setMaximumWidth(300)

        self.sidebar_layout = QtWidgets.QVBoxLayout(self.sidebar_frame)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar_layout.setSpacing(0)

        # Логотип
        self.setup_logo()

        # Кнопки навигации
        self.setup_navigation_buttons()

        # Информация о приложении
        self.setup_app_info()

    def setup_logo(self):
        """Настройка логотипа в боковой панели"""
        self.logo_frame = QtWidgets.QFrame()
        self.logo_frame.setMaximumHeight(200)

        self.logo_layout = QtWidgets.QHBoxLayout(self.logo_frame)
        self.logo_layout.setContentsMargins(0, 0, 0, 0)

        self.logo_label = ClickableLabel()
        self.logo_label.setPixmap(QtGui.QPixmap("app/gui/images/logo.jpg"))
        self.logo_label.setScaledContents(True)
        self.logo_label.setAlignment(QtCore.Qt.AlignCenter)

        self.logo_layout.addWidget(self.logo_label)
        self.sidebar_layout.addWidget(self.logo_frame)

    def setup_navigation_buttons(self):
        """Настройка кнопок навигации"""
        self.nav_buttons_frame = QtWidgets.QFrame()

        self.nav_buttons_layout = QtWidgets.QVBoxLayout(self.nav_buttons_frame)
        self.nav_buttons_layout.setContentsMargins(0, 20, 0, 0)
        self.nav_buttons_layout.setSpacing(10)

        # Кнопки
        self.matches_button = QtWidgets.QPushButton("МАТЧИ")
        self.players_button = QtWidgets.QPushButton("ИГРОКИ")
        self.teams_button = QtWidgets.QPushButton("КОМАНДЫ")

        # Добавление кнопок
        self.nav_buttons_layout.addWidget(self.matches_button)
        self.nav_buttons_layout.addWidget(self.players_button)
        self.nav_buttons_layout.addWidget(self.teams_button)

        self.sidebar_layout.addWidget(self.nav_buttons_frame, 0, QtCore.Qt.AlignTop)

    def setup_app_info(self):
        """Настройка информации о приложении"""
        self.app_info_frame = QtWidgets.QFrame()

        self.app_info_layout = QtWidgets.QVBoxLayout(self.app_info_frame)
        self.app_info_layout.setContentsMargins(0, 0, 0, 0)

        self.app_info_label = QtWidgets.QLabel("GameTracker ver. 1.0.0")
        self.app_info_label.setObjectName('app_info_label')
        self.app_info_label.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeft)

        self.app_info_layout.addWidget(self.app_info_label)
        self.sidebar_layout.addWidget(self.app_info_frame)

    def setup_main_content(self):
        """Настройка основного контента"""
        self.main_content_frame = QtWidgets.QFrame()

        self.main_content_layout = QtWidgets.QHBoxLayout(self.main_content_frame)
        self.main_content_layout.setContentsMargins(0, 0, 0, 0)

        # Виджет с переключаемыми страницами
        self.stacked_widget = QtWidgets.QStackedWidget(self.main_content_frame)
        self.stacked_widget.setFrameShape(QtWidgets.QFrame.Box)

        # Создание страниц
        self.setup_main_page()
        self.setup_matches_page()
        self.setup_players_page()
        self.setup_teams_page()
        self.setup_match_detail_page()
        self.setup_player_detail_page()
        self.setup_team_detail_page()

        self.main_content_layout.addWidget(self.stacked_widget)


    def setup_main_page(self):
        """Настройка главной страницы"""
        self.main_page = QtWidgets.QWidget()
        self.main_page_layout = QtWidgets.QVBoxLayout(self.main_page)
        self.main_page_layout.setContentsMargins(0, 0, 0, 0)
        self.main_page_layout.setSpacing(0)

        # Заголовок
        self.main_header = QtWidgets.QFrame()
        self.main_header.setFixedHeight(50)

        self.main_header_layout = QtWidgets.QGridLayout(self.main_header)
        self.main_header_label = QtWidgets.QLabel("НОВОСТИ")
        self.main_header_label.setProperty('class', 'TitleLabel')
        self.main_header_label.setAlignment(QtCore.Qt.AlignCenter)

        self.main_header_layout.addWidget(self.main_header_label, 0, 0, 1, 1)
        self.main_page_layout.addWidget(self.main_header)

        self.stacked_widget.addWidget(self.main_page)

    def setup_matches_page(self):
        """Настройка страницы матчей"""
        self.matches_page = QtWidgets.QWidget()
        self.matches_layout = QtWidgets.QGridLayout(self.matches_page)
        self.matches_layout.setContentsMargins(0, 0, 0, 0)
        self.matches_layout.setSpacing(0)

        # Контейнер для содержимого
        self.matches_container = QtWidgets.QFrame()
        self.matches_container_layout = QtWidgets.QVBoxLayout(self.matches_container)
        self.matches_container_layout.setContentsMargins(0, 0, 0, 0)
        self.matches_container_layout.setSpacing(5)

        # Заголовок
        self.matches_header = QtWidgets.QFrame()
        self.matches_header.setFixedHeight(50)
        self.matches_header.setFrameShape(QtWidgets.QFrame.Box)

        self.matches_header_layout = QtWidgets.QHBoxLayout(self.matches_header)
        self.matches_header_layout.setContentsMargins(10, 0, 10, 0)

        # Лейбл "МАТЧИ" слева
        self.matches_header_label = QtWidgets.QLabel("МАТЧИ")
        self.matches_header_label.setProperty('class', 'TitleLabel')
        self.matches_header_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        # Строка поиска
        self.matches_search = QtWidgets.QLineEdit()
        self.matches_search.setPlaceholderText("Поиск матчей...")
        search_icon = QIcon("app/gui/images/search.png")
        self.matches_search.addAction(search_icon, QtWidgets.QLineEdit.LeadingPosition)

        # Добавляем элементы в заголовок
        self.matches_header_layout.addWidget(self.matches_header_label)
        self.matches_header_layout.addWidget(self.matches_search)

        self.matches_container_layout.addWidget(self.matches_header)

        # Список матчей
        self.matches_list_frame = QtWidgets.QFrame()
        self.matches_list_layout = QtWidgets.QGridLayout(self.matches_list_frame)

        self.matches_scroll = QtWidgets.QScrollArea()
        self.matches_scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.matches_scroll.setWidgetResizable(True)

        self.matches_scroll_content = QtWidgets.QWidget()
        self.matches_scroll_layout = QtWidgets.QVBoxLayout(self.matches_scroll_content)
        self.matches_scroll_layout.setContentsMargins(0, 0, 0, 10)
        self.matches_scroll_layout.setSpacing(0)
        self.matches_scroll_layout.setAlignment(QtCore.Qt.AlignTop)

        # Добавление матчей
        self.all_match_widgets = []

        for match in all_matches:
            team1 = next((team for team in all_teams if match.team1_id == team.team_id), None)
            team2 = next((team for team in all_teams if match.team2_id == team.team_id), None)

            versus_widget = VersusWidget(
                team1.logo, team1.team_name, team1.country,
                team2.logo, team2.team_name, team2.country
            )
            self.all_match_widgets.append(versus_widget)
            self.matches_scroll_layout.addWidget(versus_widget)

            # Создаем замыкание с явным сохранением значений
            def temp_match_handler(m, t1, t2):
                return lambda: self.handle_match_click(m, t1, t2)
            versus_widget.clicked.connect(temp_match_handler(match, team1, team2))

        self.matches_scroll.setWidget(self.matches_scroll_content)
        self.matches_list_layout.addWidget(self.matches_scroll, 0, 0, 1, 1)
        self.matches_container_layout.addWidget(self.matches_list_frame, 0)

        self.matches_layout.addWidget(self.matches_container, 0, 0, 1, 1)
        self.stacked_widget.addWidget(self.matches_page)

        # Подключение строки поиска
        self.matches_search.textChanged.connect(self.handle_matches_search)

    def setup_players_page(self):
        """Настройка страницы игроков"""
        self.players_page = QtWidgets.QWidget()
        self.players_layout = QtWidgets.QGridLayout(self.players_page)
        self.players_layout.setContentsMargins(0, 0, 0, 0)
        self.players_layout.setSpacing(0)

        # Контейнер для содержимого
        self.players_container = QtWidgets.QFrame()
        self.players_container_layout = QtWidgets.QVBoxLayout(self.players_container)
        self.players_container_layout.setContentsMargins(0, 0, 0, 0)
        self.players_container_layout.setSpacing(5)

        # Заголовок
        self.players_header = QtWidgets.QFrame()
        self.players_header.setFixedHeight(50)
        self.players_header.setFrameShape(QtWidgets.QFrame.Box)

        self.players_header_layout = QtWidgets.QHBoxLayout(self.players_header)
        self.players_header_layout.setContentsMargins(10, 0, 10, 0)
        self.players_header_label = QtWidgets.QLabel("ИГРОКИ")
        self.players_header_label.setProperty('class', 'TitleLabel')
        self.players_header_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        # Строка поиска
        self.players_search = QtWidgets.QLineEdit()
        self.players_search.setPlaceholderText("Поиск игроков...")
        search_icon = QIcon("app/gui/images/search.png")
        self.players_search.addAction(search_icon, QtWidgets.QLineEdit.LeadingPosition)

        # Добавляем элементы в заголовок
        self.players_header_layout.addWidget(self.players_header_label)
        self.players_header_layout.addWidget(self.players_search)

        self.players_container_layout.addWidget(self.players_header)

        # Список игроков
        self.players_list_frame = QtWidgets.QFrame()
        self.players_list_frame.setMinimumHeight(300)
        self.players_list_layout = QtWidgets.QGridLayout(self.players_list_frame)

        self.players_scroll = QtWidgets.QScrollArea()
        self.players_scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.players_scroll.setWidgetResizable(True)

        self.players_scroll_content = QtWidgets.QWidget()
        self.players_scroll_content.setGeometry(QtCore.QRect(0, 0, 870, 298))
        self.players_scroll_layout = QtWidgets.QVBoxLayout(self.players_scroll_content)
        self.players_scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.players_scroll_layout.setAlignment(QtCore.Qt.AlignTop)

        # Добавление игроков
        self.all_player_widgets = []

        for player in all_players:
            player_widget = PlayerWidget(
                self.split_first_last_name(player)[2],
                player.country,
                player.avatar
            )
            self.all_player_widgets.append(player_widget)
            self.players_scroll_layout.addWidget(player_widget)

            def temp_player_handler(p):
                return lambda: self.handle_player_click(p)
            player_widget.clicked.connect(temp_player_handler(player))

        self.players_scroll.setWidget(self.players_scroll_content)
        self.players_list_layout.addWidget(self.players_scroll, 0, 0, 1, 1)
        self.players_container_layout.addWidget(self.players_list_frame, 0)

        self.players_layout.addWidget(self.players_container, 0, 0, 1, 1)
        self.stacked_widget.addWidget(self.players_page)

        # Подключение поиска игроков
        self.players_search.textChanged.connect(self.handle_players_search)

    def setup_teams_page(self):
        """Настройка страницы команд"""
        self.teams_page = QtWidgets.QWidget()
        self.teams_layout = QtWidgets.QGridLayout(self.teams_page)
        self.teams_layout.setContentsMargins(0, 0, 0, 0)
        self.teams_layout.setHorizontalSpacing(0)

        # Контейнер для содержимого
        self.teams_container = QtWidgets.QFrame()
        self.teams_container_layout = QtWidgets.QVBoxLayout(self.teams_container)
        self.teams_container_layout.setContentsMargins(0, 0, 0, 0)
        self.teams_container_layout.setSpacing(5)

        # Заголовок
        self.teams_header = QtWidgets.QFrame()
        self.teams_header.setFixedHeight(50)
        self.teams_header.setFrameShape(QtWidgets.QFrame.Box)

        self.teams_header_layout = QtWidgets.QHBoxLayout(self.teams_header)
        self.teams_header_layout.setContentsMargins(10, 0, 10, 0)
        self.teams_header_label = QtWidgets.QLabel("КОМАНДЫ")
        self.teams_header_label.setProperty('class', 'TitleLabel')
        self.teams_header_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        # Строка поиска
        self.teams_search = QtWidgets.QLineEdit()
        self.teams_search.setPlaceholderText("Поиск команд...")
        search_icon = QIcon("app/gui/images/search.png")
        self.teams_search.addAction(search_icon, QtWidgets.QLineEdit.LeadingPosition)

        # Добавляем элементы в заголовок
        self.teams_header_layout.addWidget(self.teams_header_label)
        self.teams_header_layout.addWidget(self.teams_search)

        self.teams_container_layout.addWidget(self.teams_header)

        # Список команд
        self.teams_list_frame = QtWidgets.QFrame()
        self.teams_list_layout = QtWidgets.QGridLayout(self.teams_list_frame)

        self.teams_scroll = QtWidgets.QScrollArea()
        self.teams_scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.teams_scroll.setWidgetResizable(True)

        self.teams_scroll_content = QtWidgets.QWidget()
        self.teams_scroll_content.setGeometry(QtCore.QRect(0, 0, 872, 85))
        self.teams_scroll_layout = QtWidgets.QVBoxLayout(self.teams_scroll_content)
        self.teams_scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.teams_scroll_layout.setAlignment(QtCore.Qt.AlignTop)

        # Добавление команд
        self.all_team_widgets = []

        for team in all_teams:
            team_widget = PlayerWidget(
                str(team.team_name),
                str(team.country),
                team.logo
            )
            self.all_team_widgets.append(team_widget)
            self.teams_scroll_layout.addWidget(team_widget)

            def temp_team_handler(t):
                return lambda: self.handle_team_click(t)
            team_widget.clicked.connect(temp_team_handler(team))

        self.teams_scroll.setWidget(self.teams_scroll_content)
        self.teams_list_layout.addWidget(self.teams_scroll, 0, 0, 1, 1)
        self.teams_container_layout.addWidget(self.teams_list_frame, 0)

        self.teams_layout.addWidget(self.teams_container, 0, 0, 1, 1)
        self.stacked_widget.addWidget(self.teams_page)

        # Подключение поиска команд
        self.teams_search.textChanged.connect(self.handle_teams_search)

    def setup_match_detail_page(self):
        """Настройка страницы деталей матча"""
        self.match_page = QtWidgets.QWidget()
        self.match_layout = QtWidgets.QVBoxLayout(self.match_page)
        self.match_layout.setContentsMargins(0, 0, 0, 0)
        self.match_layout.setSpacing(0)

        # Заголовок
        self.match_header = QtWidgets.QFrame()
        self.match_header.setFixedHeight(50)
        self.match_header.setFrameShape(QtWidgets.QFrame.Box)

        self.match_header_layout = QtWidgets.QGridLayout(self.match_header)
        self.match_name_label = QtWidgets.QLabel("МАТЧ")
        self.match_name_label.setProperty('class', 'TitleLabel')
        self.match_name_label.setAlignment(QtCore.Qt.AlignCenter)

        self.match_header_layout.addWidget(self.match_name_label, 0, 0, 1, 1)
        self.match_layout.addWidget(self.match_header)

        # Основное содержимое
        self.match_content = QtWidgets.QFrame()
        self.match_content_layout = QtWidgets.QHBoxLayout(self.match_content)
        self.match_content_layout.setContentsMargins(0, 0, 0, 0)
        self.match_content_layout.setSpacing(0)

        # Команда 1
        self.team1_frame = QtWidgets.QFrame()
        self.team1_layout = QtWidgets.QVBoxLayout(self.team1_frame)
        self.team1_layout.setContentsMargins(0, 0, 0, 0)
        self.team1_layout.setSpacing(0)

        self.team1_header = QtWidgets.QFrame()
        self.team1_header.setFixedHeight(60)

        self.team1_header_layout = QtWidgets.QGridLayout(self.team1_header)
        self.team1_name_label = QtWidgets.QLabel("Team1")
        self.team1_name_label.setProperty('class', 'TitleLabel')
        self.team1_name_label.setAlignment(QtCore.Qt.AlignCenter)

        self.team1_header_layout.addWidget(self.team1_name_label, 0, 0, 1, 1)
        self.team1_layout.addWidget(self.team1_header)

        # Игроки команды 1
        self.team1_players = QtWidgets.QFrame()
        self.team1_players_layout = QtWidgets.QVBoxLayout(self.team1_players)
        self.team1_players_layout.setContentsMargins(0, 0, 0, 0)

        for i in range(5):
            player_widget = PlayerWidget(f'Player {i}', 'Country', 'app/gui/images/user.png')
            self.team1_players_layout.addWidget(player_widget)

        self.team1_layout.addWidget(self.team1_players, 0, QtCore.Qt.AlignTop)
        self.match_content_layout.addWidget(self.team1_frame)

        # Центральная часть (карта и счет)
        self.match_center = QtWidgets.QFrame()
        self.match_center_layout = QtWidgets.QVBoxLayout(self.match_center)
        self.match_center_layout.setContentsMargins(0, 0, 0, 0)
        self.match_center_layout.setSpacing(0)

        self.map_header = QtWidgets.QFrame()
        self.map_header.setFixedHeight(60)

        self.map_header_layout = QtWidgets.QGridLayout(self.map_header)
        self.map_header_layout.setContentsMargins(0, 0, 0, 0)
        self.map_header_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.map_name_label = QtWidgets.QLabel("Inferno")
        self.map_name_label.setProperty('class', 'TitleLabel')
        self.map_name_label.setAlignment(QtCore.Qt.AlignCenter)

        self.map_header_layout.addWidget(self.map_name_label, 0, 0, 1, 1)
        self.match_center_layout.addWidget(self.map_header)

        self.map_content = QtWidgets.QFrame()
        self.map_content_layout = QtWidgets.QGridLayout(self.map_content)

        self.map_image = QtWidgets.QLabel()
        self.map_image.setMaximumSize(QtCore.QSize(300, 300))
        self.map_image.setPixmap(QtGui.QPixmap("app/gui/images/maps/Inferno.png").scaled(self.map_image.size(), QtCore.Qt.KeepAspectRatio))
        self.map_image.setScaledContents(True)
        self.map_image.setAlignment(QtCore.Qt.AlignCenter)

        self.score_label = QtWidgets.QLabel("12-4")
        self.score_label.setProperty('class', 'TitleLabel')
        self.score_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        self.map_content_layout.addWidget(self.map_image, 0, 0, 1, 1)
        self.map_content_layout.addWidget(self.score_label, 1, 0, 1, 1)
        self.match_center_layout.addWidget(self.map_content)
        self.match_content_layout.addWidget(self.match_center)

        # Команда 2
        self.team2_frame = QtWidgets.QFrame()
        self.team2_layout = QtWidgets.QVBoxLayout(self.team2_frame)
        self.team2_layout.setContentsMargins(0, 0, 0, 0)
        self.team2_layout.setSpacing(0)

        self.team2_header = QtWidgets.QFrame()
        self.team2_header.setFixedHeight(60)

        self.team2_header_layout = QtWidgets.QGridLayout(self.team2_header)
        self.team2_name_label = QtWidgets.QLabel("Team2")
        self.team2_name_label.setProperty('class', 'TitleLabel')
        self.team2_name_label.setAlignment(QtCore.Qt.AlignCenter)

        self.team2_header_layout.addWidget(self.team2_name_label, 0, 0, 1, 1)
        self.team2_layout.addWidget(self.team2_header)

        # Игроки команды 2
        self.team2_players = QtWidgets.QFrame()
        self.team2_players_layout = QtWidgets.QVBoxLayout(self.team2_players)
        self.team2_players_layout.setContentsMargins(0, 0, 0, 0)

        for i in range(5):
            player_widget = PlayerWidget(f'Player {i}', 'Country', 'app/gui/images/user.png')
            self.team2_players_layout.addWidget(player_widget)

        self.team2_layout.addWidget(self.team2_players, 0, QtCore.Qt.AlignTop)
        self.match_content_layout.addWidget(self.team2_frame)

        self.match_layout.addWidget(self.match_content)
        self.stacked_widget.addWidget(self.match_page)

    def setup_player_detail_page(self):
        """Настройка страницы деталей игрока"""
        self.player_page = QtWidgets.QWidget()
        self.player_layout = QtWidgets.QGridLayout(self.player_page)
        self.player_layout.setContentsMargins(0, 0, 0, 0)
        self.player_layout.setSpacing(0)

        # Контейнер
        self.player_container = QtWidgets.QFrame()
        self.player_container_layout = QtWidgets.QHBoxLayout(self.player_container)
        self.player_container_layout.setContentsMargins(0, 0, 0, 0)
        self.player_container_layout.setSpacing(0)

        # Левая часть (аватар)
        self.player_left = QtWidgets.QFrame()
        self.player_left.setMaximumWidth(250)
        self.player_left_layout = QtWidgets.QVBoxLayout(self.player_left)
        self.player_left_layout.setContentsMargins(0, 0, 0, 0)
        self.player_left_layout.setSpacing(0)

        # Аватар
        self.player_avatar_frame = QtWidgets.QFrame()
        self.player_avatar_frame.setMaximumHeight(250)
        self.player_avatar_layout = QtWidgets.QGridLayout(self.player_avatar_frame)

        self.player_avatar = QtWidgets.QLabel()
        self.player_avatar.setFrameShape(QtWidgets.QFrame.Box)
        self.player_avatar.setMaximumSize(QtCore.QSize(200, 200))
        self.player_avatar.setPixmap(QtGui.QPixmap("app/gui/images/user.png"))
        self.player_avatar.setScaledContents(True)

        self.player_avatar_layout.addWidget(self.player_avatar, 0, 0, 1, 1)
        self.player_left_layout.addWidget(self.player_avatar_frame)

        # Текст под аватаром
        self.player_under_avatar = QtWidgets.QFrame()
        self.player_under_avatar_layout = QtWidgets.QGridLayout(self.player_under_avatar)

        self.player_under_avatar_label = QtWidgets.QLabel("<html><head/><body><p><br/></p></body></html>")
        self.player_under_avatar_label.setObjectName('player_under_avatar_label')
        self.player_under_avatar_label.setTextFormat(QtCore.Qt.RichText)
        self.player_under_avatar_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        self.player_under_avatar_layout.addWidget(self.player_under_avatar_label, 0, 0, 1, 1)
        self.player_left_layout.addWidget(self.player_under_avatar)
        self.player_container_layout.addWidget(self.player_left)

        # Правая часть (информация)
        self.player_info_frame = QtWidgets.QFrame()
        self.player_info_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.player_info_layout = QtWidgets.QGridLayout(self.player_info_frame)

        self.player_info_label = QtWidgets.QLabel("""
            <html><head/><body>
                <p>Фамилия: Зайцев</p>
                <p>Имя: Александр</p>
                <p>Никнейм: Zayac</p>
                <p>Страна: Россия</p>
                <p>E-Mail: овиалоывиловылвыоат</p>
                <p>Телефон: 88005353535</p>
            </body></html>
        """)
        self.player_info_label.setObjectName('player_info_label')
        self.player_info_label.setTextFormat(QtCore.Qt.RichText)
        self.player_info_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        self.player_info_layout.addWidget(self.player_info_label, 0, 0, 1, 1)
        self.player_container_layout.addWidget(self.player_info_frame)

        self.player_layout.addWidget(self.player_container, 0, 0, 1, 1)
        self.stacked_widget.addWidget(self.player_page)

    def setup_team_detail_page(self):
        """Настройка страницы деталей команды"""
        self.team_page = QtWidgets.QWidget()
        self.team_layout = QtWidgets.QGridLayout(self.team_page)
        self.team_layout.setContentsMargins(0, 0, 0, 0)
        self.team_layout.setSpacing(0)

        # Контейнер
        self.team_container = QtWidgets.QFrame()
        self.team_container_layout = QtWidgets.QHBoxLayout(self.team_container)
        self.team_container_layout.setContentsMargins(0, 0, 0, 0)
        self.team_container_layout.setSpacing(0)

        # Левая часть (игроки)
        self.team_left = QtWidgets.QFrame()
        self.team_left_layout = QtWidgets.QVBoxLayout(self.team_left)
        self.team_left_layout.setContentsMargins(0, 0, 0, 0)
        self.team_left_layout.setSpacing(0)

        # Заголовок с названием команды
        self.team_name_frame = QtWidgets.QFrame()
        self.team_name_frame.setFixedHeight(50)
        self.team_name_layout = QtWidgets.QGridLayout(self.team_name_frame)
        self.team_name_layout.setContentsMargins(0, 0, 0, 0)
        self.team_name_layout.setSpacing(0)

        self.team_name_label = QtWidgets.QLabel("ClanZaicev")
        self.team_name_label.setProperty('class', 'TitleLabel')
        self.team_name_label.setFrameShape(QtWidgets.QFrame.Box)
        self.team_name_label.setAlignment(QtCore.Qt.AlignCenter)

        self.team_name_layout.addWidget(self.team_name_label, 0, 0, 1, 1)
        self.team_left_layout.addWidget(self.team_name_frame)

        # Игроки команды
        self.team_players_frame = QtWidgets.QFrame()
        self.team_players_layout = QtWidgets.QVBoxLayout(self.team_players_frame)
        self.team_players_layout.setContentsMargins(0, 0, 0, 0)

        for i in range(5):
            player_widget = PlayerWidget(f'Player {i}', 'Country', 'app/gui/images/user.png')
            self.team_players_layout.addWidget(player_widget)

        self.team_left_layout.addWidget(self.team_players_frame, 0, QtCore.Qt.AlignTop)
        self.team_container_layout.addWidget(self.team_left)

        # Правая часть (аватар и информация)
        self.team_right = QtWidgets.QFrame()
        self.team_right.setFrameShape(QtWidgets.QFrame.Box)
        self.team_right_layout = QtWidgets.QVBoxLayout(self.team_right)
        self.team_right_layout.setContentsMargins(0, 0, 0, 0)
        self.team_right_layout.setSpacing(0)

        # Аватар команды
        self.team_avatar_frame = QtWidgets.QFrame()
        self.team_avatar_frame.setMaximumHeight(200)
        self.team_avatar_layout = QtWidgets.QGridLayout(self.team_avatar_frame)

        self.team_avatar = QtWidgets.QLabel()
        self.team_avatar.setFrameShape(QtWidgets.QFrame.Box)
        self.team_avatar.setMaximumSize(QtCore.QSize(150, 150))
        self.team_avatar.setPixmap(QtGui.QPixmap("app/gui/images/user.png"))
        self.team_avatar.setScaledContents(True)
        self.team_avatar.setAlignment(QtCore.Qt.AlignCenter)

        self.team_avatar_layout.addWidget(self.team_avatar, 0, 0, 1, 1)
        self.team_right_layout.addWidget(self.team_avatar_frame)

        # Информация о команде
        self.team_info_frame = QtWidgets.QFrame()
        self.team_info_layout = QtWidgets.QGridLayout(self.team_info_frame)

        self.team_info_label = QtWidgets.QLabel("""
            <html><head/><body>
                <p>Страна: Россия</p>
            </body></html>
        """)
        self.team_info_label.setObjectName('team_info_label')
        self.team_info_label.setTextFormat(QtCore.Qt.RichText)
        self.team_info_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        self.team_info_layout.addWidget(self.team_info_label, 0, 0, 1, 1)
        self.team_right_layout.addWidget(self.team_info_frame)
        self.team_container_layout.addWidget(self.team_right)

        self.team_layout.addWidget(self.team_container, 0, 0, 1, 1)
        self.stacked_widget.addWidget(self.team_page)

    def setup_connections(self):
        """Настройка соединений между элементами интерфейса"""
        self.logo_label.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.matches_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.players_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.teams_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))

        # 0 - новости(page_main) - 0
        # 1 - page_match - 4
        # 2 - page_matches - 1
        # 3 - page_players - 2
        # 4 - page_teams - 3
        # 5 - page_player
        # 6 - page_team

    # Обработка нажатия по записям ----------------------------------------------------
    def handle_match_click(self, match, team1, team2):
        """Обработка клика по матчу с отображением полной информации"""
        try:
            mapa = [mp for mp in all_maps if mp.map_id == match.map_id][0]
            # Обновляем основные данные матча
            self.match_name_label.setText(f"{team1.team_name} vs {team2.team_name}")
            self.team1_name_label.setText(team1.team_name)
            self.team2_name_label.setText(team2.team_name)
            self.map_name_label.setText(mapa.map_name)

            # Устанавливаем логотипы команд
            # set_widget_image(self.team1_logo, team1.logo)  # Предполагается, что team1_logo существует
            # set_widget_image(self.team2_logo, team2.logo)  # Предполагается, что team2_logo существует

            # Устанавливаем карту
            set_widget_image(self.map_image, mapa.image)

            # Устанавливаем счет
            if match.team1_score and match.team2_score:
                self.score_label.setText(f"{match.team1_score}-{match.team2_score}\n{match.match_status}")
            else:
                self.score_label.setText(f"{match.match_status}")

            # Очищаем предыдущие составы команд
            for i in reversed(range(self.team1_players_layout.count())):
                self.team1_players_layout.itemAt(i).widget().setParent(None)
            for i in reversed(range(self.team2_players_layout.count())):
                self.team2_players_layout.itemAt(i).widget().setParent(None)

            # Получаем составы команд для этого матча
            match_lineups = [ml for ml in all_match_lineups if ml.match_id == match.match_id]

            # Добавляем игроков команды 1
            team1_lineup = [ml for ml in match_lineups if ml.team_id == team1.team_id]
            for lineup in team1_lineup:
                player = next((p for p in all_players if p.player_id == lineup.player_id), None)
                if player:
                    player_widget = PlayerWidget(
                        f'"{player.nickname}"',
                        player.country,
                        player.avatar
                    )
                    self.team1_players_layout.addWidget(player_widget)

                    # def temp_player_handler(t):
                    #     return lambda: self.handle_player_click(t)
                    # player_widget.clicked.connect(temp_player_handler(player))

            # Добавляем игроков команды 2
            team2_lineup = [ml for ml in match_lineups if ml.team_id == team2.team_id]
            for lineup in team2_lineup:
                player = next((p for p in all_players if p.player_id == lineup.player_id), None)
                if player:
                    player_widget = PlayerWidget(
                        f'"{player.nickname}"',
                        player.country,
                        player.avatar
                    )
                    self.team2_players_layout.addWidget(player_widget)

                    # def temp_player_handler(t):
                    #     return lambda: self.handle_player_click(t)
                    # player_widget.clicked.connect(temp_player_handler(player))

            # Переключаемся на страницу матча
            self.stacked_widget.setCurrentIndex(4)
        except Exception as ex:
            print(ex)

    def handle_player_click(self, player):
        # Установка аватара
        set_widget_image(self.player_avatar, player.avatar)

        self.player_info_label.setText(f"""
                    <html><head/><body>
                        <p>Фамилия: {self.split_first_last_name(player)[1]}</p>
                        <p>Имя: {self.split_first_last_name(player)[0]}</p>
                        <p>Никнейм: {player.nickname}</p>
                        <p>Страна: {player.country}</p>
                        <p>Дата рождения: {player.date_of_birth}</p>
                        <p>E-Mail: {player.email}</p>
                        <p>Телефон: {player.phone}</p>
                        <p>STEAM_ID: {player.steam_id}</p>
                    </body></html>
                """)

        self.stacked_widget.setCurrentIndex(5)

    def handle_team_click(self, team):
        # Установка аватара
        set_widget_image(self.team_avatar, team.logo)

        self.team_name_label.setText(team.team_name)

        self.team_info_label.setText(f"""
                    <html><head/><body>
                        <p>Страна: {team.country}</p>
                    </body></html>
                """)

        # Очищаем игроков команды
        for i in reversed(range(self.team_players_layout.count())):
            widget = self.team_players_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Получаем состав команды
        team_lineups = [lp for lp in all_team_lineups if team.team_id == lp.team_id]
        if not team_lineups:
            return

        # Добавляем игроков команды
        for lineup in team_lineups:
            player = next((pl for pl in all_players if lineup.player_id == pl.player_id), None)
            if player is not None:
                player_widget = PlayerWidget(
                    self.split_first_last_name(player)[2],
                    player.country,
                    player.avatar
                )
                self.team_players_layout.addWidget(player_widget)

                # Подключаем обработчик клика
                # def temp_player_handler(t):
                #     return lambda: self.handle_player_click(t)
                # player_widget.clicked.connect(temp_player_handler(player))

        self.stacked_widget.setCurrentIndex(6)

    # Обработка поиска ----------------------------------------------------------------
    def handle_matches_search(self):
        search_text = self.matches_search.text().lower().strip()

        if not search_text:
            # Если строка поиска пуста - показать все элементы
            for widget in self.all_match_widgets:
                widget.show()
            return

        for widget in self.all_match_widgets:

            team1_name = str(getattr(widget, 'team1_name', ''))
            team1_country = str(getattr(widget, 'team1_country', ''))
            team2_name = str(getattr(widget, 'team2_name', ''))
            team2_country = str(getattr(widget, 'team2_country', ''))

            match_found = (search_text in team1_name.lower() or
                           search_text in team1_country.lower() or
                           search_text in team2_name.lower() or
                           search_text in team2_country.lower())

            widget.setVisible(match_found)

    def handle_players_search(self):
        search_text = self.players_search.text().lower().strip()

        if not search_text:
            # Если строка поиска пуста - показать все элементы
            for widget in self.all_player_widgets:
                widget.show()
            return

        for widget in self.all_player_widgets:

            player_name = str(getattr(widget, 'text1', ''))
            player_country = str(getattr(widget, 'text2', ''))

            player_found = (search_text in player_name.lower() or
                           search_text in player_country.lower())

            widget.setVisible(player_found)

    def handle_teams_search(self):
        search_text = self.teams_search.text().lower().strip()

        if not search_text:
            # Если строка поиска пуста - показать все элементы
            for widget in self.all_team_widgets:
                widget.show()
            return

        for widget in self.all_team_widgets:
            team_name = str(getattr(widget, 'text1', ''))
            team_country = str(getattr(widget, 'text2', ''))

            player_found = (search_text in team_name.lower() or
                            search_text in team_country.lower())

            widget.setVisible(player_found)