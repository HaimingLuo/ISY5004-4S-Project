from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFileDialog, QLineEdit, QScrollArea, QGridLayout, QProgressBar, QMessageBox
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QPixmap

class InputTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
            }
            QPushButton {
                padding: 20px 40px;
                font-size: 24px;
                font-family: Arial, sans-serif;
                border: none;
                border-radius: 10px;
                color: white;
                cursor: pointer;
                margin: 10px 0;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            QPushButton#upload_button {
                background-color: rgb(47, 92, 160);
            }
            QPushButton#upload_button:hover {
                background-color: rgb(40, 78, 136);
            }
            QPushButton#submit_button {
                background-color: rgb(180, 92, 0);
                color: white;
            }
            QPushButton#submit_button:hover {
                background-color: rgb(150, 77, 0);
            }
            QPushButton#submit_button:disabled {
                background-color: #cccccc;
                color: white;
                cursor: not-allowed;
            }
            QLineEdit {
                padding: 15px;
                font-size: 24px;
                font-family: Arial, sans-serif;
                border: 1px solid #ccc;
                border-radius: 8px;
                background-color: #f8f8f8;
                color: #333;
                margin: 10px 0;
            }
            QLineEdit:focus {
                border-color: #66afe9;
                outline: none;
            }
            QProgressBar {
                height: 45px;
                font-size: 24px;
                font-family: Arial, sans-serif;
                border: none;
                border-radius: 8px;
                background-color: #e0e0e0;
                text-align: center;
                color: #333;
            }
            QProgressBar::chunk {
                background-color: rgb(40, 180, 40);
                border-radius: 8px;
            }
        """)
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setSpacing(40)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # Left side layout
        self.image_layout = QGridLayout()
        self.image_layout.setSpacing(10)

        image_widget = QWidget()
        image_widget.setLayout(self.image_layout)

        main_layout.addWidget(image_widget, 2)

        # Right side layout
        right_layout = QVBoxLayout()
        right_layout.setSpacing(20)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.addStretch()

        self.upload_button = QPushButton("Upload Images")
        self.upload_button.setObjectName("upload_button")
        self.upload_button.clicked.connect(self.upload_images)
        right_layout.addWidget(self.upload_button)

        self.input_text = QLineEdit()
        self.input_text.setPlaceholderText("Enter category")
        right_layout.addWidget(self.input_text)

        self.submit_button = QPushButton("Submit")
        self.submit_button.setObjectName("submit_button")
        self.submit_button.clicked.connect(self.submit)
        self.submit_button.setEnabled(False)  # Initially disable the submit button
        right_layout.addWidget(self.submit_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p%")
        right_layout.addWidget(self.progress_bar)

        right_layout.addStretch()
        right_layout.setAlignment(Qt.AlignBottom | Qt.AlignHCenter)
        main_layout.addLayout(right_layout, 1)
        self.setLayout(main_layout)

    def upload_images(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", "Images Files (*.png *.jpg *.jpeg)", options=options)
        if files:
            for file in files:
                self.show_image(file)
            self.submit_button.setEnabled(True)  # Enable the submit button if images are uploaded
        else:
            self.submit_button.setEnabled(False)  # Disable the submit button if no images are uploaded

    def show_image(self, file_path):
        pixmap = QPixmap(file_path)
        pixmap = pixmap.scaledToWidth(200, Qt.SmoothTransformation)  # Resize to 200 width
        label = QLabel()
        label.setPixmap(pixmap)
        label.setStyleSheet("""
            QLabel {
                border: 4px solid #ccc;
                border-radius: 20px;
                background-color: black;
            }
        """)
        label.setAlignment(Qt.AlignCenter)

        # Calculate the row and column based on the current count
        count = self.image_layout.count()
        row = count // 3
        col = count % 3

        # Only add the image if there is space in the grid
        if count < 9:  # Maximum 3 rows of 3 images
            self.image_layout.addWidget(label, row, col)

    def submit(self):
        category = self.input_text.text()
        if category:
            print(f"Submitted category: {category}")
            self.input_text.clear()
            self.start_progress_bar()

    def start_progress_bar(self):
        self.progress_bar.setValue(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress_bar)
        self.timer.start(30)  # Timer set to 30ms for a total of 3 seconds (100 steps)

    def update_progress_bar(self):
        value = self.progress_bar.value() + 1
        self.progress_bar.setValue(value)
        if value >= 100:
            self.timer.stop()
            self.show_message_box("New gesture added successfully")

    def show_message_box(self, message):
        # Clear left side images
        for i in reversed(range(self.image_layout.count())):
            widget = self.image_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Reset progress bar
        self.progress_bar.reset()
        self.progress_bar.setValue(0)  # Set progress bar value to 0%

        # Change submit button color to green for 2 seconds
        self.submit_button.setStyleSheet("""
            QPushButton#submit_button {
                background-color: #4CAF50;
                color: white;
            }
        """)
        QTimer.singleShot(2000, self.reset_submit_button_color)

        # Show message box
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle("Notification")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

        # Reset to initial state
        self.input_text.clear()
        for i in reversed(range(self.image_layout.count())):
            widget = self.image_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Ensure progress bar shows percentage after reset
        self.progress_bar.setFormat("%p%")

        # Disable the submit button after submission
        self.submit_button.setEnabled(False)

    def reset_submit_button_color(self):
        self.submit_button.setStyleSheet("""
            QPushButton#submit_button {
                background-color: rgb(180, 92, 0);
                color: white;
            }
            QPushButton#submit_button:hover {
                background-color: rgb(150, 77, 0);
            }
        """)
