import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Engine and Tech Assembly")
        self.setGeometry(100, 100, 400, 200)

        # Dictionary to store form values
        self.data = {"Engine Type": "", "Tech Assembly": 3, "Components": 1}

        # Layout
        main_layout = QVBoxLayout()

        # Engine Type Entry
        engine_layout = QHBoxLayout()
        engine_label = QLabel("Engine Type:")
        self.engine_entry = QLineEdit()
        engine_layout.addWidget(engine_label)
        engine_layout.addWidget(self.engine_entry)
        main_layout.addLayout(engine_layout)

        # Tech Assembly Entry
        tech_layout = QHBoxLayout()
        tech_label = QLabel("Tech Assembly:")
        self.tech_entry = QLineEdit()
        self.tech_entry.setReadOnly(True)  # Read-only field for displaying the value
        self.tech_entry.setText("3")  # Starting value
        tech_layout.addWidget(tech_label)
        tech_layout.addWidget(self.tech_entry)
        main_layout.addLayout(tech_layout)

        # Submit button
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit_form)
        main_layout.addWidget(submit_button)

        self.setLayout(main_layout)

    def submit_form(self):
        # Retrieve values from form fields
        engine_type = self.engine_entry.text()
        tech_assembly = int(self.tech_entry.text())

        # Update dictionary with new values
        self.data["Engine Type"] = engine_type
        self.data["Tech Assembly"] = tech_assembly

        # Print the dictionary
        print(self.data)

        # Reset form
        self.engine_entry.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
