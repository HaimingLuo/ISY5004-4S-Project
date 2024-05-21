
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QTimer
import cv2
from tabs.recognition_tab import RecognitionTab
from tabs.learning_tab import LearningTab
from tabs.input_tab import InputTab

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
                padding: 15px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                font-size: 30px;
                min-width: 300px;
                min-height: 45px;
                font-family: 'Microsoft YaHei', sans-serif;
            }
            QTabBar::tab:selected {
                background-color: #a9a9a9;
            }
            QLabel {
                font-size: 30px;
                color: #333333;
                font-family: 'Microsoft YaHei', sans-serif;
            }
            QProgressBar {
                font-size: 30px;
                border-radius: 10px;
                text-align: center;
                background-color: #e0e0e0;
                font-family: 'Microsoft YaHei', sans-serif;
            }
        """)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        tab_layout = QHBoxLayout()
        tab_layout.addStretch(1)
        
        tab_widget = QTabWidget()
        tab_widget.addTab(RecognitionTab(), "Recognition")
        tab_widget.addTab(LearningTab(), "Learning")
        tab_widget.addTab(InputTab(), "Input")
        
        tab_layout.addWidget(tab_widget)
        tab_layout.addStretch(1)
        
        layout.addLayout(tab_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
