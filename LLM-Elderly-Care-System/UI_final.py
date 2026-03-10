import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QStackedWidget
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, QSize, QThread, pyqtSignal
import sounddevice as sd
import wavio
from FUNCTION_final import transcribe_audio, handle_file_upload, Neo4jGPTQuery, translate_to_chinese, translate_to_english, preprocess_question
import os
from openai import OpenAI

# 初始化 Neo4jGPTQuery 
url = "bolt://localhost:7687"  # Neo4j URL
user = "neo4j"
password = "bbbb1234"


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
user_name = "Benny" 
neo4j_gpt = Neo4jGPTQuery(url, user, password, api_key, user_name)


fs = 44100  # 採樣
seconds = 5  # 錄音時間
audio_file_path = 'output.wav'  # 錄音的文件path

def format_response(response):
    if isinstance(response, list):
        formatted = '; '.join([', '.join(map(str, sublist)) for sublist in response])
    elif isinstance(response, str):
        formatted = response
    else:
        formatted = str(response)
    return formatted

class RecordThread(QThread):
    finished = pyqtSignal(str)

    def run(self):
        print("Recording...")
        recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()
        wavio.write(audio_file_path, recording, fs, sampwidth=2)
        print("Recording stopped.")
        self.finished.emit(audio_file_path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("讓我陪你一起")
        self.resize(800, 600)

        # 字體
        app = QApplication.instance()
        font = QFont("標楷體", 14)
        app.setFont(font)

        
        app.setStyleSheet("""
            QPushButton {
                background-color: #fffff5;
                color: #7C7877;
                border: 1.5px solid #C6B9AF;
                padding: 10px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #E6D5B5;
            }
            QWidget {
                background-color: #F9F3EE;
            }
        """)

        #初始化UI
        self.initUI()
        self.neo4j_gpt = Neo4jGPTQuery("bolt://localhost:7687", "neo4j", "bbbb1234", "OpenAIKey", "Benny")

    def initUI(self):
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        # Start Screen
        self.start_screen = QWidget()
        start_layout = QVBoxLayout()
        
        image_label = QLabel()
        pixmap = QPixmap('start_screen_2.jpg')
        scaled_pixmap = pixmap.scaled(QSize(800, 600), Qt.AspectRatioMode.KeepAspectRatio)
        image_label.setPixmap(scaled_pixmap)
        image_label.setScaledContents(True)  # 讓圖片填满label
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        start_layout.addWidget(image_label)
        
        start_chat_button = QPushButton("開始聊天")
        start_chat_button.clicked.connect(self.show_chat_screen)
        start_layout.addWidget(start_chat_button)
        
        self.start_screen.setLayout(start_layout)
        self.stacked_widget.addWidget(self.start_screen)

        # Chat Screen
        self.chat_screen = QWidget()
        chat_layout = QVBoxLayout()
        
        self.gpt_response_box = QTextEdit()
        self.gpt_response_box.setPlaceholderText("顯示GPT回應的文字訊息")
        self.gpt_response_box.setReadOnly(True)
        chat_layout.addWidget(self.gpt_response_box)

        self.input_box = QTextEdit()
        self.input_box.setPlaceholderText("顯示輸入的語音轉文字")
        chat_layout.addWidget(self.input_box)
        
        button_layout = QHBoxLayout()
        record_button = QPushButton("錄音")
        record_button.clicked.connect(self.start_recording)
        send_button = QPushButton("發送")
        send_button.clicked.connect(self.send_audio_and_process)
        main_screen_button = QPushButton("主畫面")
        main_screen_button.clicked.connect(self.show_start_screen)
        button_layout.addWidget(record_button)
        button_layout.addWidget(send_button)
        button_layout.addWidget(main_screen_button)
        
        chat_layout.addLayout(button_layout)
        self.chat_screen.setLayout(chat_layout)
        self.stacked_widget.addWidget(self.chat_screen)
        
        self.record_thread = RecordThread()
        self.record_thread.finished.connect(self.process_audio)
        #return self.chat_screen 

    def show_start_screen(self):
        self.stacked_widget.setCurrentWidget(self.start_screen)

    def show_chat_screen (self):
        self.stacked_widget.setCurrentWidget(self.chat_screen )

    def start_recording(self):
        self.record_thread.start()

    def process_audio(self):
        transcription = transcribe_audio('output.wav')
        self.input_box.setPlainText(f"我: {transcription}")

    def send_audio_and_process(self):
        try:
            response = handle_file_upload('output.wav', neo4j_gpt)
            translated_response = translate_to_chinese(response)
            formatted_response = format_response(translated_response)
            self.gpt_response_box.setPlainText(f"回答: {formatted_response}")
        except Exception as e:
            self.gpt_response_box.setPlainText(f"Error: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
