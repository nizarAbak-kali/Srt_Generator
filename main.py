import sys
import time
import signal
import datetime
from PyQt5.Qt import QTimer
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, \
    QPushButton, QHBoxLayout


class Timer(QMainWindow) :

    def __init__(self, parent=None, filename="", srt_num=0):

        QMainWindow.__init__(self)
        self.srt_filename = filename
        self.start_time = time.time()
        self.srt_number = srt_num
        self.last_subtitle_time = None
        # init de l 'interface Qt
        self.initUI()

        # gestion des signaux
        print( "My lovely timer!" )
        signal.signal(signal.SIGINT, self.signal_handler)

        # initialisation du timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.timer.start(1000)


    def initUI(self):
        self.form_widget = FormWidget(self)
        _widget = QWidget()
        _layout = QVBoxLayout(_widget)
        _layout.addWidget(self.form_widget)
        self.setCentralWidget(_widget)
        self.form_widget.write_button.clicked.connect(self.handlebutton)

        self.setGeometry(100, 100, 800, 200)
        self.setWindowTitle("start counting Mongrel !")

    def tick(self):
        #print( str(time.sftime())
        y = time.time() - self.start_time
        self.current_time = str(datetime.timedelta(seconds=int(y)))
        # numero du sous-titre
        self.form_widget.srt_label.setText(str(self.srt_number)+"\n")
        # le delta entre deux le debut et la fin
        self.form_widget.delta.setText(str(self.last_subtitle_time) + " --> " + str(self.current_time) + "\n")
        # le debut du timer
        self.form_widget.label_time.setText(self.current_time)

        print( self.current_time )
        print("tick" )

    def handlebutton(self):
        self.last_subtitle_time = self.current_time

        with open(self.srt_filename, "a") as f:
            text = str(self.srt_number)+ "\n" + \
                self.last_subtitle_time + " --> " +self.current_time + "\n"+ \
                str(self.form_widget.txted.text()) + "\n \n"
            f.write(text)
            f.close()

        self.srt_number = self.srt_number + 1

    def signal_handler(self,*args):
        """handle pour le signal SIGINT"""
        sys.stderr.write("\r")
        if QMessageBox.question(None, "lol", "Voulez-vous quitter ?",
                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
            QApplication.quit()


class FormWidget(QWidget):

    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)
        self.__controls()
        self.__layout()

    def __controls(self):
        self.label = QLabel("Nombre de personne : ")
        self.txted = QLineEdit()
        self.lbled = QLabel("Open/close")
        self.cmbox = QComboBox()
        self.label_time = QLabel()
        self.write_button = QPushButton("write buffer", self)
        self.srt_label = QLabel()
        self.delta = QLabel()

    def __layout(self):
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.h2Box = QHBoxLayout()
        self.h3box = QHBoxLayout()
        self.h4box = QHBoxLayout()

        self.hbox.addWidget(self.label)
        self.hbox.addWidget(self.txted)

        self.h2Box.addWidget(self.lbled)
        self.h2Box.addWidget(self.cmbox)

        self.h3box.addWidget(self.label_time)
        self.h3box.addWidget(self.write_button)

        self.h4box.addWidget(self.srt_label)
        self.h4box.addWidget(self.delta)

        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(self.h2Box)
        self.vbox.addLayout(self.h3box)
        self.vbox.addLayout(self.h4box)

        self.setLayout(self.vbox)

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    name = sys.argv[1]
    timer = Timer(sys.argv, name)
    timer.show()

    sys.exit(app.exec_())


# run event loop so python doesn't exit
if __name__ == "__main__":

    main()
