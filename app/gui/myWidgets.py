from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtCore import pyqtSignal


class ClickableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)


class PlayerWidget(QWidget):
    def __init__(self, player_data=None, parent=None):
        super().__init__(parent)
        self.player = player_data


class VersusWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("Versus Widget")