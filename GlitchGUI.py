import sys
import GlitchManager as GlitchManager
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QFileDialog, QWidget, QLabel
from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget

class MainWindow(QMainWindow):
    def __init__(self, glitch_manager):
        super().__init__()

        self.setWindowTitle("FFGlitch")
        self.setGeometry(100, 100, 800, 600)
        self.glitch_manager: GlitchManager = glitch_manager
        self.num_glitches = 0

        #Init Widgets
        self.video_player = VideoPlayer()

        self.setCentralWidget(self.video_player)


        # init file path, bake, preprocess, and glitch button ui

        # init glitch list ui

        # init video uis

    def open_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'All Files (*);;Text Files (*.txt)', options=options)

        if file_path:
            print(f'Selected file path: {file_path}')
            self.file_path_label.setText(f'Selected file path: {file_path}')
            self.glitch_manager.set_input_file_path(file_path)
    
    def open_folder(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder', options=options)

        # Update the label with the selected folder path
        if folder_path:
            self.folder_path_label.setText(f'Selected folder path: {folder_path}')

    def pre_process(self):
        # Register Button Press
        self.glitch_manager.preprocess(self)

    def bake(self):
        # Register Button Press
        self.glitch_manager.bake(self)

    def add_glitch(self):
        # Register button and pull info from GUI to call add
        pass

    def update_glitch(self):
        # Register button and pull info from GUI to call update
        pass

    def delete_glitch(self):
        # Register button and pull info from GUI to call delete
        pass

    def get_glitch(self):
        # Register button and pull info from GUI to call get
        pass

class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VideoPlayer")
        self.setGeometry(100, 100, 800, 600)
        # self.player = QMediaPlayer()
        # self.player.setSource(QUrl.fromLocalFile("/Users/alex/Projects/Code/glitch_editor/inputs/IMG_0013.MOV"))
        # self.videoWidget = QVideoWidget()
        # self.player.setVideoOutput(self.videoWidget)

        # Video Player Controls

        # Set/Rest Video Player Source