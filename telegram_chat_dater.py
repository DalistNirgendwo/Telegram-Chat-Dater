import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import matplotlib.pyplot as plt
import json
import pandas as pd


def fileloader(file):
    f = open(file, encoding='utf-8')
    data = json.load(f)
    f.close()
    return data


def popper(data):
    size = len(data["messages"])
    # dates = {}
    ls = ["".join(["0", str(i)]) for i in range(10)]
    ls.extend([str(i) for i in range(10, 24)])
    time = {ls[i]: 0 for i in range(24)}

    # pop non-needed lines
    datelist = [data["messages"][i]['date'][:10] for i in range(size)]
    timelist = [data["messages"][i]['date'][11:-6] for i in range(size)]

    for i in range(size):
        datelist[i] = datelist[i].replace('-01', '-1')
        datelist[i] = datelist[i].replace('-02', '-2')
        datelist[i] = datelist[i].replace('-03', '-3')
        datelist[i] = datelist[i].replace('-04', '-4')
        datelist[i] = datelist[i].replace('-05', '-5')
        datelist[i] = datelist[i].replace('-06', '-6')
        datelist[i] = datelist[i].replace('-07', '-7')
        datelist[i] = datelist[i].replace('-08', '-8')
        datelist[i] = datelist[i].replace('-09', '-9')

    startdate = datelist[0]
    enddate = datelist[-1]
    daterange = pd.date_range(start=startdate, end=enddate)
    dates = {
        f"{daterange[i].year}-{daterange[i].month}-{daterange[i].day}": 0 for i in range(len(daterange))}

    # count days
    for i in range(size):
        dates[datelist[i]] += 1

    for i in range(size):
        time[timelist[i]] += 1

    for i in time:
        time[i] = time[i] / size

    plt.figure(figsize=(20, 12))
    plt.subplot(211)
    plt.bar(*zip(*dates.items()))
    plt.xticks(rotation=90)
    plt.subplot(212)
    plt.bar(*zip(*time.items()))
    plt.show()

    return dates


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Telegram Chat Dater'
        self.left = 100
        self.top = 100
        self.width = 300
        self.height = 100
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        comboBox = QComboBox(self)
        comboBox.move(100, 60)

        button = QPushButton('Load file', self)
        button.setToolTip('Click this button to load a .json file.')
        button.move(100, 40)
        button.clicked.connect(self.openFileNameDialog)
        # button.clicked.connect(self.comboBox.addItem("Schwanz"))

        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "", "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)
            # popper(fileloader(fileName))
            # for i in range(5):
            #     self.initUI().comboBox.addItem(f"{i}")
            self.comboBox2 = QComboBox(self)
       


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
