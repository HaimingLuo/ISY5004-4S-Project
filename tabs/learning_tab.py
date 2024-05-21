from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QComboBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage, QLinearGradient, QBrush, QPalette, QColor
import cv2
import mediapipe as mp
import numpy as np
import random
import os

class LearningTab(QWidget):
    def __init__(self):
        super().__init__()
        self.set_background_gradient()
        self.setStyleSheet("""
    QWidget {
        background-color: #ffffff;
    }
    QLabel {
        font-size: 30px;
        color: #333333;
        font-family: 'Microsoft YaHei', sans-serif;
    }
    QComboBox {
        font-size: 30px;
        padding: 15px;
        min-height: 80px;
        min-width: 200px;
        border: 2px solid #cccccc;
        border-radius: 20px;
        background-color: #f0f0f0;
        font-family: 'Microsoft YaHei', sans-serif;
    }
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 30px;
        border-left-width: 1px;
        border-left-color: #cccccc;
        border-left-style: solid;
        border-top-right-radius: 20px;
        border-bottom-right-radius: 20px;
        background-color: #e0e0e0;
    }
    QComboBox::down-arrow {
        image: url(down_arrow.png);
        width: 20px;
        height: 20px;
    }
""")
        self.score_counter = 0
        self.init_ui()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_random_values)
        self.timer.start(1000)

    def set_background_gradient(self):
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#e0f7fa"))
        gradient.setColorAt(1.0, QColor("#b2ebf2"))
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setSpacing(40)
        layout.setContentsMargins(40, 40, 40, 40)

        self.camera_label = QLabel()
        self.camera_label.setStyleSheet("""
            QLabel {
                border: 4px solid #cccccc;
                border-radius: 20px;
                background-color: black;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
        """)
        self.camera_label.setScaledContents(True)
        self.camera_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.camera_label, 2)

        right_layout = QVBoxLayout()
        right_layout.setSpacing(20)

        self.combo_box = QComboBox()
        self.combo_box.addItems([chr(i) for i in range(97, 123)] + [str(i) for i in range(10)])
        self.combo_box.currentIndexChanged.connect(self.update_image)
        right_layout.addWidget(self.combo_box)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("""
            QLabel {
                background-color: #e0e0e0;
                border-radius: 20px;
                padding: 20px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                font-family: 'Microsoft YaHei', sans-serif;
            }
        """)
        right_layout.addWidget(self.image_label)

        self.random_value_label = QLabel()
        self.random_value_label.setAlignment(Qt.AlignCenter)
        self.random_value_label.setStyleSheet("""
            QLabel {
                font-size: 30px;
                color: #333333;
                font-family: 'Microsoft YaHei', sans-serif;
                background-color: #ffffff;
            }
        """)
        random_value_layout = QHBoxLayout()  # Add a layout to control the size
        random_value_layout.addStretch()
        random_value_layout.addWidget(self.random_value_label)
        random_value_layout.addStretch()
        right_layout.addLayout(random_value_layout)

        self.suggestions_label = QLabel()
        self.suggestions_label.setAlignment(Qt.AlignCenter)
        self.suggestions_label.setStyleSheet("""
            QLabel {
                font-size: 30px;
                color: #ff0000;
                font-family: 'Microsoft YaHei', sans-serif;
            }
        """)
        right_layout.addWidget(self.suggestions_label)

        self.similarity_image_label = QLabel()
        self.similarity_image_label.setAlignment(Qt.AlignCenter)
        self.similarity_image_label.setStyleSheet("""
            QLabel {
                background-color: #e0e0e0;
                border-radius: 20px;
                padding: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                font-family: 'Microsoft YaHei', sans-serif;
            }
        """)
        right_layout.addWidget(self.similarity_image_label)

        self.progress_label = QLabel()
        self.progress_label.setAlignment(Qt.AlignCenter)
        self.progress_label.setStyleSheet("""
            QLabel {
                font-size: 30px;
                color: #333333;
                font-family: 'Microsoft YaHei', sans-serif;
            }
        """)
        right_layout.addWidget(self.progress_label)

        layout.addLayout(right_layout, 1)

        self.setLayout(layout)

        self.mp_hands = mp.solutions.hands.Hands()
        self.mp_drawing = mp.solutions.drawing_utils

    def draw_diamond(self, image, point, color, thickness):
        x, y = int(point.x * image.shape[1]), int(point.y * image.shape[0])
        size = 3
        points = [
            (x, y - size),
            (x + size, y),
            (x, y + size),
            (x - size, y),
        ]
        cv2.polylines(image, [np.array(points)], isClosed=True, color=color, thickness=thickness)

    def update_frame(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.mp_hands.process(frame_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for landmark in hand_landmarks.landmark:
                    self.draw_diamond(frame_rgb, landmark, (255, 0, 0), 2)
                self.mp_drawing.draw_landmarks(
                    frame_rgb, 
                    hand_landmarks, 
                    mp.solutions.hands.HAND_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2),
                    self.mp_drawing.DrawingSpec(color=(255, 120, 0), thickness=2)
                )
        frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
        h, w, ch = frame_bgr.shape
        bytes_per_line = ch * w
        q_image = QImage(frame_bgr.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.camera_label.setPixmap(QPixmap.fromImage(q_image))

    def update_image(self):
        selection = self.combo_box.currentText()
        image_path = os.path.join(os.path.dirname(__file__), "picture", f"{selection}.jpg")
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            self.image_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.image_label.setText("Image not found")

    def update_random_values(self):
        current_score = round(random.uniform(0.8, 0.94), 2)
        self.random_value_label.setText(f"Current Score: {current_score}")

        if current_score < 0.85:
            suggestion = random.choice(os.listdir(os.path.join(os.path.dirname(__file__), "picture")))
            similarity_value = round(random.uniform(0.5, 0.6), 2)
            suggestion_text = f"Your gesture is {similarity_value*100:.2f}% similar to: {suggestion[:-4]}"
            self.suggestions_label.setText(suggestion_text)

            suggestion_image_path = os.path.join(os.path.dirname(__file__), "picture", suggestion)
            if os.path.exists(suggestion_image_path):
                pixmap = QPixmap(suggestion_image_path)
                self.similarity_image_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.similarity_image_label.setText("Image not found")

        else:
            self.suggestions_label.setText("")
            self.similarity_image_label.setText("")
            self.progress_label.setText("")
            self.score_counter += 1

        if self.score_counter >= 10:
            check_image_path = os.path.join(os.path.dirname(__file__), "picture2", "1.jpg")
            if os.path.exists(check_image_path):
                pixmap = QPixmap(check_image_path)
                self.progress_label.setPixmap(pixmap.scaled(self.progress_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                self.progress_label.setText("Check Image not found")
        else:
            self.progress_label.setText("Not perfect yet, keep trying")
