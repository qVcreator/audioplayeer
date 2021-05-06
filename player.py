import vlc
import sys
import os
import random
import time
from mutagen.mp3 import MP3
from PyQt5 import QtWidgets
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *
from ui import Ui_MainWindow

class Player(QtWidgets.QMainWindow):
    action = 'stop'
    song = 0
    is_mixed = 0
    def __init__(self):
        super(Player, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_5.clicked.connect(self.choose_folder)
        self.ui.pushButton.clicked.connect(self.play)
        self.ui.pushButton_2.clicked.connect(self.stop)
        self.ui.pushButton_4.clicked.connect(self.next)
        self.ui.pushButton_3.clicked.connect(self.previous)
        self.ui.pushButton_6.clicked.connect(self.mix_playlist)        

    def next(self):
        if Player.action != 'stop':
            Player.action = 'change'
            if Player.song == self.max_songs:
                Player.song = 0
            else:
                Player.song += 1
            self.play()
            

    def previous(self):
        if Player.action != 'stop':
            Player.action = 'change'
            if Player.song == 0 - self.max_songs:
                Player.song = 0
            else:
                Player.song -= 1
            self.play()


    def mix_playlist(self):
        try:
            self.ui.textBrowser.clear()
            if Player.is_mixed == 0:
                self.playlist = []
                mixed_files = []
                for i in self.files:
                    if (i[-3:]) == 'mp3':
                        mixed_files.append(i)
                for i in range(len(mixed_files)-1, 0, -1):
                    j = random.randint(0, i + 1)
                    mixed_files[i], mixed_files[j] = mixed_files[j], mixed_files[i]
                for i in mixed_files:
                    self.playlist.append(self.dirlist+'/'+i)
                    self.ui.textBrowser.append(i)
                Player.is_mixed = 1
            elif Player.is_mixed == 1:
                for i in self.files:
                    if (i[-3:]) == 'mp3':
                        self.playlist.append(self.dirlist+'/'+i)
                        self.ui.textBrowser.append(i)
                Player.is_mixed = 0
        except:
            self.ui.pushButton_6.setChecked(0)
            pass

    def stop(self):
        try:
            self.music.pause()
            self.ui.timer.stop()
            Player.action = 'pause'
        except:
            pass

    def play(self):
        try:
            if Player.action == 'stop' or Player.action == 'play':
                self.music = vlc.MediaPlayer(self.playlist[Player.song])
                self.music.play()
                Player.action = 'play'
            elif Player.action == 'change':
                self.music.stop()
                self.music = vlc.MediaPlayer(self.playlist[Player.song])
                self.music.play()
                Player.action = 'play'
            elif Player.action == 'pause':
                self.music.play()     

            if self.ui.timer.isActive():
                self.ui.step = 0
                self.ui.progressBar.setValue(self.ui.step)
            else:
                self.ui.timer.start(1000, self)
        except AttributeError:
            pass

    def choose_folder(self):
        try:
            self.playlist = []
            self.ui.textBrowser.clear()
            self.dirlist = QFileDialog.getExistingDirectory(self,"Выбрать папку",".")
            self.files = os.listdir(self.dirlist)
            for i in self.files:
                if (i[-3:]) == 'mp3':
                    self.playlist.append(self.dirlist+'/'+i)
                    self.ui.textBrowser.append(i)
            self.max_songs = len(self.playlist) - 1
        except PermissionError:
            self.show_error()

    def timerEvent(self, e):
        end_song = MP3(self.playlist[Player.song]).info.length
        self.ui.progressBar.setMaximum(end_song)
        if self.ui.step >= end_song:
            self.ui.step = 0
            Player.song += 1
            print(Player.action)
            self.play()
            return
        self.ui.step = self.ui.step + 1
        self.ui.progressBar.setValue(self.ui.step)

    def show_error(self):
        self.l_error = errors()

class errors(QWidget):

    def __init__(self):
        super().__init__()
        self.link_error()

    def link_error(self):
        self.window_error = QWidget()
        self.layout_er = QVBoxLayout()

        self.layout_er.addWidget(QLabel('<h2>Ошибка прав доступа<h2>', alignment=QtCore.Qt.AlignCenter))
        self.layout_er.addWidget(QLabel('<h4>Запустите приложение от имени администратора<h4>', alignment=QtCore.Qt.AlignCenter))

        self.ok_button = QPushButton('OK')
        self.layout_er.addWidget(self.ok_button, alignment=QtCore.Qt.AlignCenter)
        
        self.ok_button.clicked.connect(self.link_error_close)

        self.window_error.setFixedSize(225, 90)

        self.window_error.setWindowTitle('ERROR')
        self.window_error.setLayout(self.layout_er)
        self.window_error.show()
    
    def link_error_close(self):
        self.window_error.close()
        
def main():
    app = QtWidgets.QApplication(sys.argv)
    application = Player()
    application.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()