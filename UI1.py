import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QLineEdit, QMessageBox, QScrollArea, QProgressBar)
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt, QTimer
import cv2
import mediapipe as mp
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sign Language Recognition System")
        self.setGeometry(100, 100, 1920, 1080)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTabWidget::pane {
                border: none;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 15px; /* 缩小高度为原来的75% */
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                font-size: 24px; /* 缩小字体为原来的75% */
                min-width: 200px;
                min-height: 45px; /* 缩小高度为原来的75% */
            }+
            QTabBar::tab:selected {
                background-color: #ffffff;
            }
            QLabel {
                font-size: 24px; /* 缩小字体为原来的75% */
                color: #333333;
            }
            QProgressBar {
                font-size: 24px; /* 统一进度条字体 */
                border-radius: 10px; /* 增加圆角 */
                text-align: center;
                background-color: #e0e0e0; /* 进度条背景色 */
            }
        """)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        tab_widget = QTabWidget()
        self.recognition_tab = RecognitionTab()
        self.learning_tab = LearningTab()
        self.input_tab = InputTab()
        tab_widget.addTab(self.recognition_tab, "Sign Recognition")
        tab_widget.addTab(self.learning_tab, "Sign Learning")
        tab_widget.addTab(self.input_tab, "Sign Input")
        tab_widget.setStyleSheet("""
            QTabWidget::tab-bar {
                alignment: center;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.addWidget(tab_widget)
        central_widget.setLayout(main_layout)

        self.camera = cv2.VideoCapture(0)
        self.camera_timer = QTimer()
        self.camera_timer.timeout.connect(self.update_camera)
        self.camera_timer.start(30)

    def update_camera(self):
        ret, frame = self.camera.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.recognition_tab.update_frame(frame)
            self.learning_tab.update_frame(frame)

    def closeEvent(self, event):
        self.camera.release()
        event.accept()

class RecognitionTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
            }
        """)
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setSpacing(40)  # 增加间距
        layout.setContentsMargins(40, 40, 40, 40)  # 增加边距

        self.camera_label = QLabel()
        self.camera_label.setStyleSheet("""
            QLabel {
                border: 4px solid #cccccc;  # 增加边框厚度
                border-radius: 20px;  # 增加圆角
                background-color: black;
            }
        """)
        self.camera_label.setScaledContents(True)
        self.camera_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.camera_label, 2)  # Make camera_label take 2/3 of the space

        self.result_label = QLabel("Recognition Result")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("""
            QLabel {
                background-color: #e0e0e0;
                border-radius: 20px;  # 增加圆角
                padding: 20px;  # 增加内边距
                font-size: 30px;  # 缩小字体为原来的75%
                color: #333333;
            }
        """)
        layout.addWidget(self.result_label, 1)  # Make result_label take 1/3 of the space

        self.setLayout(layout)

        self.mp_hands = mp.solutions.hands.Hands()
        self.mp_drawing = mp.solutions.drawing_utils

    def draw_diamond(self, image, point, color, thickness):
        x, y = int(point.x * image.shape[1]), int(point.y * image.shape[0])
        size = 3  # 调整菱形大小
        points = [
            (x, y - size),
            (x + size, y),
            (x, y + size),
            (x - size, y),
        ]
        cv2.polylines(image, [np.array(points)], isClosed=True, color=color, thickness=thickness)

    def update_frame(self, frame):
        results = self.mp_hands.process(frame)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for landmark in hand_landmarks.landmark:
                    self.draw_diamond(frame, landmark, (0, 0, 255), 2)
                self.mp_drawing.draw_landmarks(
                    frame, 
                    hand_landmarks, 
                    mp.solutions.hands.HAND_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2),
                    self.mp_drawing.DrawingSpec(color=(255, 120, 0), thickness=2)  # 橙色连接线
                )
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.camera_label.setPixmap(QPixmap.fromImage(q_image))

class LearningTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
            }
        """)
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setSpacing(40)  # 增加间距
        layout.setContentsMargins(40, 40, 40, 40)  # 增加边距

        self.camera_label = QLabel()
        self.camera_label.setStyleSheet("""
            QLabel {
                border: 4px solid #cccccc;  # 增加边框厚度
                border-radius: 20px;  # 增加圆角
                background-color: black;
            }
        """)
        self.camera_label.setScaledContents(True)
        self.camera_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.camera_label, 2)  # Make camera_label take 2/3 of the space

        self.guide_label = QLabel("Learning Guide")
        self.guide_label.setAlignment(Qt.AlignCenter)
        self.guide_label.setStyleSheet("""
            QLabel {
                background-color: #e0e0e0;
                border-radius: 20px;  # 增加圆角
                padding: 20px;  # 增加内边距
                font-size: 30px;  # 缩小字体为原来的75%
                color: #333333;
            }
        """)
        layout.addWidget(self.guide_label, 1)  # Make guide_label take 1/3 of the space

        self.setLayout(layout)

        self.mp_hands = mp.solutions.hands.Hands()
        self.mp_drawing = mp.solutions.drawing_utils

    def draw_diamond(self, image, point, color, thickness):
        x, y = int(point.x * image.shape[1]), int(point.y * image.shape[0])
        size = 3  # 调整菱形大小
        points = [
            (x, y - size),
            (x + size, y),
            (x, y + size),
            (x - size, y),
        ]
        cv2.polylines(image, [np.array(points)], isClosed=True, color=color, thickness=thickness)

    def update_frame(self, frame):
        results = self.mp_hands.process(frame)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for landmark in hand_landmarks.landmark:
                    self.draw_diamond(frame, landmark, (0, 0, 255), 2)
                self.mp_drawing.draw_landmarks(
                    frame, 
                    hand_landmarks, 
                    mp.solutions.hands.HAND_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2),
                    self.mp_drawing.DrawingSpec(color=(255, 120, 0), thickness=2)  # 橙色连接线
                )
        h, w, ch = frame.shape


        bytes_per_line = ch * w
        q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.camera_label.setPixmap(QPixmap.fromImage(q_image))

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

        # Left side scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        self.grid_layout = QGridLayout(scroll_widget)
        self.grid_layout.setSpacing(10)
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area, 2)

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

        self.mp_hands = mp.solutions.hands.Hands()
        self.mp_drawing = mp.solutions.drawing_utils

    def upload_images(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", "Images Files (*.png *.jpg *.jpeg)", options=options)
        if files:
            for file in files:
                self.show_image(file)
                self.recognize_gesture(file)  # Recognize gesture for each uploaded image
            self.submit_button.setEnabled(True)  # Enable the submit button if images are uploaded
        else:
            self.submit_button.setEnabled(False)  # Disable the submit button if no images are uploaded

    def show_image(self, file_path):
        pixmap = QPixmap(file_path)
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
        row = self.grid_layout.rowCount()
        self.grid_layout.addWidget(label, row, 0)

    def recognize_gesture(self, file_path):
        # Load the image
        image = cv2.imread(file_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image and find hand landmarks
        results = self.mp_hands.process(image_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = [(lm.x, lm.y) for lm in hand_landmarks.landmark]
                gesture = self.classify_gesture(landmarks)
                print(f"Recognized gesture: {gesture}")

    def classify_gesture(self, landmarks):
        # Placeholder simple classification based on landmarks
        # This is where you would implement your gesture classification logic
        if self.is_tiger(landmarks):
            return "Tiger"
        elif self.is_gun(landmarks):
            return "Gun"
        elif self.is_heart(landmarks):
            return "Heart"
        elif self.is_love_u(landmarks):
            return "Love U"
        elif self.is_bad(landmarks):
            return "Bad"
        else:
            return "Unknown"

    def is_tiger(self, landmarks):
        # Implement Tiger gesture classification logic here
        return False

    def is_gun(self, landmarks):
        # Implement Gun gesture classification logic here
        return False

    def is_heart(self, landmarks):
        # Implement Heart gesture classification logic here
        return False

    def is_love_u(self, landmarks):
        # Implement Love U gesture classification logic here
        return False

    def is_bad(self, landmarks):
        # Implement Bad gesture classification logic here
        return False

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
        self.timer.start(50)

    def update_progress_bar(self):
        value = self.progress_bar.value() + 1
        self.progress_bar.setValue(value)
        if value >= 100:
            self.timer.stop()
            self.show_message_box("New gesture added successfully")

    def show_message_box(self, message):
        # Clear left side images
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
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
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.png"))
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
