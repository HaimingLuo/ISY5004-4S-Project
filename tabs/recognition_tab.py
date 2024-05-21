from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QPushButton, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, QFont
import cv2
import mediapipe as mp
import numpy as np

class RecognitionTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                font-family: 'Microsoft YaHei';
                font-size: 30px;
            }
            QLabel {
                font-family: 'Microsoft YaHei';
                font-size: 30px;
            }
            QPushButton {
                font-family: 'Microsoft YaHei';
                font-size: 30px;
            }
            QPushButton#normalize_button {
                background-color: #F5DEB3;  /* 米色 */
                border-radius: 10px;  /* 圆角 */
                padding: 10px;  /* 内边距 */
            }
            QTextEdit {
                font-family: 'Microsoft YaHei';
                font-size: 30px;
                border: 1px solid #cccccc;
                border-radius: 10px;
                padding: 10px;
                background-color: #f8f8f8;
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

        right_layout = QVBoxLayout()
        right_layout.setSpacing(20)

        self.result_label = QLabel("Recognition Result")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("""
            QLabel {
                background-color: #e0e0e0;
                border-radius: 20px;  # 增加圆角
                padding: 20px;  # 增加内边距
                font-size: 30px;
                color: #333333;
            }
        """)
        right_layout.addWidget(self.result_label)

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Enter text here...")
        right_layout.addWidget(self.text_edit)

        self.normalize_button = QPushButton("Normalization")
        self.normalize_button.setObjectName("normalize_button")  # 设置对象名
        self.normalize_button.clicked.connect(self.normalize_text)
        right_layout.addWidget(self.normalize_button)

        self.normalized_text_edit = QTextEdit()
        self.normalized_text_edit.setReadOnly(True)
        self.normalized_text_edit.setFixedHeight(self.text_edit.height())  # 设置与上面文本框相同的高度
        right_layout.addWidget(self.normalized_text_edit)

        layout.addLayout(right_layout, 1)  # Make right_layout take 1/3 of the space

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

    def normalize_text(self):
        normalized_text = "I am NUS student. I love NUS."
        self.normalized_text_edit.setText(normalized_text)