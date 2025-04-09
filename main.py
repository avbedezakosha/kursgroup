import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton
from app.gui.main_window import MainWindow, AdminWindow


class RoleDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.role = None
        self.setWindowTitle("Выбор роли")
        layout = QVBoxLayout()
        self.admin_btn = QPushButton("admin")
        self.user_btn = QPushButton("user")

        layout.addWidget(self.admin_btn)
        layout.addWidget(self.user_btn)
        self.setLayout(layout)

        self.admin_btn.clicked.connect(self.select_admin)
        self.user_btn.clicked.connect(self.select_user)

    def select_admin(self):
        self.role = "admin"
        self.accept()

    def select_user(self):
        self.role = "user"
        self.accept()


def main():
    app = QApplication(sys.argv)

    role_dialog = RoleDialog()
    if role_dialog.exec_() == QDialog.Accepted:
        if role_dialog.role == "admin":
            window = AdminWindow()
        else:
            window = MainWindow()

    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
