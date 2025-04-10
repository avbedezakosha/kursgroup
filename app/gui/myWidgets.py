from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QApplication, QFrame
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QPixmap, QFont


class PlayerWidget(QWidget):
    clicked = pyqtSignal()  # Определяем сигнал

    def __init__(self, text1, text2, image_path='user.png', parent=None):
        super().__init__(parent)

        # Настройки основного виджета (прозрачный фон)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedHeight(100)  # 100px контент + 2px сверху + 2px снизу

        # Фоновая "рамка" (только по краям)
        self.border_frame = QFrame(self)
        self.border_frame.setStyleSheet("background: transparent; border-radius: 10px;")
        self.border_frame.setFixedSize(self.width(), self.height())

        # Основной контент (с отступами 2px от краев)
        content_widget = QWidget()
        content_widget.setFixedHeight(100)
        content_widget.setStyleSheet("background: transparent;")

        # Layout с контентом (ваш оригинальный код)
        layout = QHBoxLayout(content_widget)
        layout.setContentsMargins(15, 15, 15, 15)

        # Виджет для изображения
        self.image_label = QLabel()
        pixmap = QPixmap(image_path)
        self.image_label.setMaximumSize(QSize(80, 80))
        self.image_label.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        layout.addWidget(self.image_label, alignment=Qt.AlignTop)

        # Вертикальный layout для текста
        text_layout = QVBoxLayout()

        # Первая текстовая метка
        self.label1 = QLabel(text1)
        self.label1.setStyleSheet("color: white; font-size: 30px;")
        text_layout.addWidget(self.label1)

        # Вторая текстовая метка
        self.label2 = QLabel(text2)
        self.label2.setStyleSheet("color: white; font-size: 26px;")
        text_layout.addWidget(self.label2)

        text_layout.addStretch()
        layout.addLayout(text_layout)

        # Главный layout (добавляем контент с отступами)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)  # Отступы для "рамки"
        main_layout.addWidget(content_widget)

        # Включаем обработку событий мыши
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(False)
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        self.clicked.emit()  # Испускаем сигнал при нажатии
        super().mousePressEvent(event)

    def enterEvent(self, event):
        self.border_frame.setStyleSheet("background-color: rgba(200, 200, 200, 100); border-radius: 10px;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.border_frame.setStyleSheet("background-color: transparent;")
        super().leaveEvent(event)

    def resizeEvent(self, event):
        self.border_frame.setFixedSize(self.size())
        super().resizeEvent(event)


class VersusWidget(QWidget):
    clicked = pyqtSignal()

    def __init__(self,
                 left_image_path: str,
                 left_text1: str,
                 left_text2: str,
                 right_image_path: str,
                 right_text1: str,
                 right_text2: str,
                 parent=None):
        super().__init__(parent)

        # Настройки основного виджета (прозрачный фон)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedHeight(100)  # 100px контент + 2px сверху + 2px снизу

        # Фоновая "рамка" (только по краям)
        self.border_frame = QFrame(self)
        self.border_frame.setStyleSheet("background: transparent; border-radius: 10px;")
        self.border_frame.setFixedSize(self.width(), self.height())

        # Основной контент (с отступами 2px от краев)
        content_widget = QWidget()
        content_widget.setFixedHeight(100)
        content_widget.setStyleSheet("background: transparent;")

        # Layout с контентом (ваш оригинальный код)
        layout = QHBoxLayout(content_widget)
        layout.setContentsMargins(15, 15, 15, 15)

        # === Левый блок (картинка + вертикальный текст) ===
        left_block = QHBoxLayout()
        left_block.setSpacing(10)

        # Картинка (слева)
        left_img = QLabel()
        left_img.setFixedWidth(80)
        left_img.setPixmap(QPixmap(left_image_path).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        left_block.addWidget(left_img)

        # Вертикальный layout для текста (справа от картинки)
        left_text_layout = QVBoxLayout()
        left_text_layout.setSpacing(2)

        # Надпись 1 (30px)
        left_label1 = QLabel(str(left_text1))
        left_label1.setStyleSheet("color: white; font-size: 30px;")
        left_text_layout.addWidget(left_label1)

        # Надпись 2 (26px)
        left_label2 = QLabel(str(left_text2))
        left_label2.setStyleSheet("color: white; font-size: 26px;")
        left_text_layout.addWidget(left_label2)

        left_block.addLayout(left_text_layout)
        layout.addLayout(left_block)

        # Центральная надпись
        vs_label = QLabel("VS")
        vs_label.setFont(QFont("Arial", 40, QFont.Bold))
        vs_label.setStyleSheet("color: white;")
        layout.addWidget(vs_label, alignment=Qt.AlignCenter)

        # === Правый блок (вертикальный текст + картинка) ===
        right_block = QHBoxLayout()
        right_block.setSpacing(10)

        # Вертикальный layout для текста (слева от картинки)
        right_text_layout = QVBoxLayout()
        right_text_layout.setSpacing(2)

        # Надпись 1 (30px)
        right_label1 = QLabel(right_text1)
        right_label1.setStyleSheet("color: white; font-size: 30px;")
        right_text_layout.addWidget(right_label1, alignment=Qt.AlignRight)

        # Надпись 2 (26px)
        right_label2 = QLabel(str(right_text2))
        right_label2.setStyleSheet("color: white; font-size: 26px;")
        right_text_layout.addWidget(right_label2, alignment=Qt.AlignRight)

        right_block.addLayout(right_text_layout)

        # Картинка (справа)
        right_img = QLabel()
        right_img.setFixedWidth(80)
        right_img.setPixmap(QPixmap(right_image_path).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        right_block.addWidget(right_img)

        layout.addLayout(right_block)

        # Главный layout (добавляем контент с отступами)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)  # Отступы для "рамки"
        main_layout.addWidget(content_widget)

        # Настройки курсора
        self.setCursor(Qt.PointingHandCursor)

    def enterEvent(self, event):
        self.border_frame.setStyleSheet("background: rgba(200, 200, 200, 100); border-radius: 10px;")

    def leaveEvent(self, event):
        self.border_frame.setStyleSheet("background: transparent; border-radius: 10px;")

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)

    def resizeEvent(self, event):
        self.border_frame.setFixedSize(self.size())
        super().resizeEvent(event)


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)
