from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy, QScrollArea, QWidget


class CardTemplate(QFrame):
    clicked = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setFrameShape(QFrame.StyledPanel)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumWidth(300)

    def mousePressEvent(self, event):
        self.clicked.emit(self.item_id)
        super().mousePressEvent(event)


class MatchCard(CardTemplate):
    def __init__(self, match, parent=None):
        super().__init__(parent)
        self.match = match
        self.item_id = match.match_id
        self._init_ui()
        self.setStyleSheet("background: white; padding: 10px;")  # Добавляем стили

    def _init_ui(self):
        layout = QVBoxLayout(self)

        # Основная информация
        header = QHBoxLayout()
        header.addWidget(QLabel(f"Матч #{self.match.match_id}"))
        header.addStretch()
        header.addWidget(QLabel(self.match.match_status))

        # Тела карточки
        body = QHBoxLayout()
        body.addWidget(QLabel(f"Команда 1:\n{self.match.team1_id or 'Неизвестно'}"))
        body.addWidget(QLabel("VS"))
        body.addWidget(QLabel(f"Команда 2:\n{self.match.team2_id or 'Неизвестно'}"))

        # Сборка карточки
        layout.addLayout(header)
        layout.addLayout(body)
        layout.addWidget(QLabel(f"Дата: {self.match.match_date}"))


class PlayerCard(CardTemplate):
    def __init__(self, player, parent=None):
        super().__init__(parent)
        self.player = player
        self.item_id = player.player_id
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)

        # Аватар
        # avatar = QLabel()
        # avatar.setPixmap(QPixmap("default_avatar.png")
        # layout.addWidget(avatar)

        # Информация
        info = QVBoxLayout()
        info.addWidget(QLabel(f"nickname: {self.player.nickname}"))
        info.addWidget(QLabel(f"command: {self.player.steam_id}"))
        layout.addLayout(info)


class TeamCard(CardTemplate):
    def __init__(self, team, parent=None):
        super().__init__(parent)
        self.team = team
        self.item_id = team.team_id
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout(self)

        info = QVBoxLayout()
        info.addWidget(QLabel(f"name: {self.team.team_name}"))
        layout.addLayout(info)


class CardList(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)

        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)
        self.layout.setAlignment(Qt.AlignTop)
        self.setWidget(self.container)

    def add_card(self, card):
        self.layout.addWidget(card)

    def clear(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
