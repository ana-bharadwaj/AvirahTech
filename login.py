from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QGroupBox
from PyQt5.QtGui import QPixmap, QColor


class LoginWidget(QWidget):
    def __init__(self, username_label, password_label):
        super().__init__()

        self.username_label = QLabel(username_label)
        self.username_edit = QLineEdit()
        self.password_label = QLabel(password_label)
        self.password_edit = QLineEdit()
        self.submit_button = QPushButton("SUBMIT")
        # Set smaller fixed size for the button
        self.submit_button.setFixedSize(80, 25)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.submit_button)
        self.setLayout(layout)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 800, 600)  # Full screen

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()  # Main layout as QVBoxLayout

        # Blue strip navbar
        blue_strip_layout = QHBoxLayout()

        blue_strip_text = QLabel("Welcome to Login Page")
        blue_strip_text.setStyleSheet("color: white; font-weight: bold;")
        blue_strip_layout.addWidget(blue_strip_text)

        # Inserting image inside the blue navbar
        blue_strip_image = QLabel()
        pixmap = QPixmap("ins_logo.png")  # Provide the path to your image
        pixmap = pixmap.scaledToHeight(40)  # Set maximum height
        blue_strip_image.setPixmap(pixmap)
        blue_strip_layout.addWidget(blue_strip_image)

        blue_strip = QLabel()
        blue_strip.setStyleSheet("background-color: #007bff;")
        blue_strip.setFixedHeight(50)  # Set height of the navbar

        # **Add blue_strip_layout first for overlapping effect**
        main_layout.addLayout(blue_strip_layout)
        # Add the blue_strip QLabel to the main layout
        main_layout.addWidget(blue_strip)

        # User and Admin login options side by side
        login_options_layout = QHBoxLayout()

        # User login group box
        user_group_box = QGroupBox("User Login")
        user_group_box.setStyleSheet(
            "QGroupBox { font-weight: bold; border: 2px solid #007bff; border-radius: 8px; padding: 10px; }"
        )
        user_layout = QVBoxLayout()

        user_segment = LoginWidget("User ID:", "User PASSWORD:")
        user_layout.addWidget(user_segment)
        user_group_box.setLayout(user_layout)
        login_options_layout.addWidget(user_group_box)

        # Admin login group box
        admin_group_box = QGroupBox("Admin Login")
        admin_group_box.setStyleSheet(
            "QGroupBox { font-weight: bold; border: 2px solid #007bff; border-radius: 8px; padding: 10px; }"
        )
        admin_layout = QVBoxLayout()

        admin_segment = LoginWidget("Admin ID:", "Admin PASSWORD:")
        admin_layout.addWidget(admin_segment)
        admin_group_box.setLayout(admin_layout)
        login_options_layout.addWidget(admin_group_box)

        main_layout.addLayout(login_options_layout)

        # Spacer to push login options to the center
        main_layout.addStretch()

        self.setLayout(main_layout)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()  
    window.show()  
    sys.exit(app.exec_())
