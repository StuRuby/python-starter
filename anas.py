from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets, uic
from PyQt5.Qt import *
from PyQt5.QtGui import QIcon
import tkinter as tk
from tkinter import filedialog
from PyQt5.QtCore import QTimer
import wave as we
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
import PyQt5.sip
import time
import sys
################################
# FFT
import os
from scipy.fftpack import fft, ifft
import scipy.signal as signal
from pydub import AudioSegment
from PyQt5.QtWidgets import QMessageBox
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
import myui


class Stock(QMainWindow, myui.Ui_MainWindow):

    def __init__(self):

        # PyQt5 直接加载ui文件
        # 因为 第三方控件通过promote的定义
        # 已经可以知道 控件类所在模块的路径
        # self.ui = uic.loadUi("main.ui")
        QMainWindow.__init__(self)
        myui.Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # self.minHz = 0
        # self.maxHz = 0
        # self.maxdB = 0
        self.path = ''
        self.flag = 0
        self.startbuttonflag = 0
        self.row = 0
        self.col = 0
        self.ffff = 1
        self.clearflag = 0
        self.framlens = 1
        self.sliderhadmove = 0

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateData)

        self.setWarningTable()
        self.startButton.clicked.connect(self.handlestartbutton)
        self.openButton.clicked.connect(self.openfile)
        self.actionopenFile.triggered.connect(self.openfile)
        self.actioncovm4a.triggered.connect(self.covm4atowav)

        # 设置最小值
        self.playSlider.setMinimum(0)
        # 设置最大值
        # self.ui.playSlider.setMaximum(99)
        # 步长
        self.playSlider.setSingleStep(1)
        # 设置当前值
        self.playSlider.setValue(0)
        # 刻度位置，刻度在下方
        # self.playSlider.setTickPosition(QSlider.TicksBelow)
        # 设置刻度间隔
        # self.playSlider.setTickInterval(1)
        # self.playSlider.sliderReleased.connect(self.valuechange)

    # def valuechange(self):
    #     if self.path == '':
    #         pass
    #     else:
    #         print("ggg:", self.playSlider.value())
    #         self.timer.stop()
    #         self.pre = self.playSlider.value() * self.len40ms
    #         self.next = (self.playSlider.value()+1) * self.len40ms
    #         self.sliderhadmove = 1

    def openfile(self):

        filePath, _ = QFileDialog.getOpenFileName(
            self,  # 父窗口对象
            "选择音频文件",  # 标题
            os.getcwd(),  # 起始目录
            "音频类型 (*.wav)"  # 选择类型过滤项，过滤内容在括号中
        )
        self.path = filePath
        # print(self.path)
        self.fenBeiZhi.setText(str(0))
        # self.readinput()
        # self.dealaudiodata(self.path)

    def dealaudiodata(self):

        # print("888\n")
        WAVE = we.open(self.path)
        # print("999\n")
        a = WAVE.getparams().nframes  # 帧总数
        self.f = WAVE.getparams().framerate  # 采样频率
        self.sample_time = 1 / self.f  # 采样点的时间间隔
        time = a / self.f  # 声音信号的长度

        # print('a', a, 'f', self.f)
        self.sample_frequency, self.audio_sequence = wavfile.read(self.path)

        # print('audio_sequence=', len(audio_sequence))  # 声音信号每一帧的“大小”
        # print("type:\n", type(audio_sequence), audio_sequence)
        self.len40ms = int(self.framlens * self.f)
        # print("len40:", self.len40ms)
        self.fram = int(len(self.audio_sequence) / self.len40ms)
        self.playSlider.setMaximum(self.fram)
        # print("nnnmmm\n")
        # print("len40ms:", self.len40ms, "fram:", self.fram)

        self.pre = 0
        self.next = self.len40ms
        # self.calu(audio_sequence[self.pre:self.next], self.framlens, self.sample_time, f)
        WAVE.close()

    def readinput(self):
        # print("123\n")
        self.varminHz = int(self.minHz.text())
        # print("iii\n")
        self.varmaxHz = int(self.maxHz.text())

        self.varmaxdB = int(self.maxdB.text())
        '''
        WAVE = we.open(self.path)
        print('---------声音信息------------')
        
        # for item in enumerate(WAVE.getparams()):
        #     print('item：', item)
        
        a = WAVE.getparams().nframes  # 帧总数
        self.f = WAVE.getparams().framerate  # 采样频率
        self.sample_time = 1 / self.f  # 采样点的时间间隔
        time = a / self.f  # 声音信号的长度
        print('a', a, 'f', self.f)
        self.sample_frequency, self.audio_sequence = wavfile.read(self.path)
        #print('audio_sequence=', len(audio_sequence))  # 声音信号每一帧的“大小”
        #print("type:\n", type(audio_sequence), audio_sequence)
        self.len40ms = int(40 / 1000 * self.f)
        print("len40:", self.len40ms)
        self.fram = int(len(self.audio_sequence) / self.len40ms)
        print("nnnmmm\n")
        print("len40ms:", self.len40ms, "fram:", self.fram)
        self.pre = 0
        self.next = self.len40ms
        #self.calu(audio_sequence[self.pre:self.next], 0.04, self.sample_time, f)
        '''
        '''
        self.updataX = []
        self.updataY = []
        self.ui.shiyu.setLabel("left", "幅值")
        self.ui.shiyu.setLabel("bottom", "时间/s")
        self.curve1 = self.ui.shiyu.getPlotItem().plot()

        self.updatafftX = []
        self.updatafftY = []
        self.ui.pinyu.setLabel("left", "幅值")
        self.ui.pinyu.setLabel("bottom", "频率/Hz")
        self.curve2 = self.ui.pinyu.getPlotItem().plot()
        # 启动定时器，每隔1秒通知刷新一次数据
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateData)
        self.timer.start(0.04)
        '''
        # time.sleep(3)
        #self.calu(audio_sequence[1920:3840], 0.04, self.sample_time, f)
        '''
        for i in range(fram):
            print("uuu\n")
            self.calu(audio_sequence[self.pre:self.next], 0.04, self.sample_time, f)
            self.pre = self.next
            self.next = self.len40ms * (i+2)
            print("pre:", self.pre, "next:", self.next)
            z = 0
            for j in range(1000000):
                z += 1
        '''
        '''
        x_seq = np.arange(0, time, self.sample_time)
        #print('x_seq=', len(x_seq), 'f=', f)
        print("qqq\n")
        ################################
        # FFT
        yy = fft(audio_sequence)
        yreal = yy.real  # 获取实数部分
        yimag = yy.imag  # 获取虚数部分

        yf = abs(fft(audio_sequence))  # 取模
        yf1 = abs(fft(audio_sequence)) / ((len(x_seq) / 2))  # 归一化处理
        yf2 = yf1[range(int(len(x_seq) / 2))]  # 由于对称性，只取一半区间

        n = len(audio_sequence)
        k = np.arange(n) / n
        frq = f * k
        frq = frq[range(int(n / 2))]

        sound = AudioSegment.from_file(self.path, "wav")
        loudness = sound.dBFS
        loudness = loudness * (-2.0)
        print("loudness\n")
        print(loudness)
        self.ui.fenBeiZhi.setText(str(int(loudness)))
        print("eee\n")


        #hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        #temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
        self.ui.shiyu.plot(x_seq, audio_sequence * 0.001)
        self.ui.pinyu.plot(frq, yf2)
        print("ttt\n")
        findmaxHz = np.array(yf2)
        listfindmaxHz = findmaxHz.tolist()
        maxindex = listfindmaxHz.index(max(listfindmaxHz))
        #print(maxindex)
        findfrq = np.array(frq)
        if findfrq[maxindex] > self.minHz and findfrq[maxindex] < self.maxHz:
            pass

        if loudness > self.maxdB:
            pass
        '''

    def handlestartbutton(self):
        varfenBeiZhi = int(self.fenBeiZhi.text())
        if varfenBeiZhi < 0.05:
            self.framlens = 0.05
        if self.clearflag == 1:
            self.curve1.clear()
            self.curve2.clear()
        self.readinput()
        # print("777\n")
        self.dealaudiodata()
        self.updataPlot()
        '''
        if self.startbuttonflag == 0:
            self.updataPlot()
            self.ui.startButton.setText("停止")
            self.startbuttonflag = 1
        else:
            self.timer.stop()
            self.updataX = []
            self.updataY = []
            self.updatafftX = []
            self.updatafftY = []
            self.ui.startButton.setText("开始")
            self.startbuttonflag = 0
        '''

    def updataPlot(self):
        self.updataX = []
        self.updataY = []
        self.shiyu.setLabel("left", "幅值")
        self.shiyu.setLabel("bottom", "时间/s")
        self.curve1 = self.shiyu.getPlotItem().plot()

        self.updatafftX = []
        self.updatafftY = []
        self.pinyu.setLabel("left", "幅值/dB")
        self.pinyu.setLabel("bottom", "频率/Hz")

        self.curve2 = self.pinyu.getPlotItem().plot()
        # 启动定时器，每隔1秒通知刷新一次数据
        # self.timer = QtCore.QTimer()
        # self.timer.timeout.connect(self.updateData)
        self.timer.start(self.framlens)

    def calu(self, audio_sequence, time, sample_time, f):
        x_seq = np.arange(0, time, sample_time)
        # print('x_seq=', len(x_seq), 'f=', f)
        # print("qqq\n")
        # print("len audio:", len(audio_sequence), "data:", audio_sequence)
        ################################
        # FFT
        yy = fft(audio_sequence)
        # print("yy\n")
        yreal = yy.real  # 获取实数部分
        yimag = yy.imag  # 获取虚数部分

        yf = abs(fft(audio_sequence))  # 取模
        yf1 = abs(fft(audio_sequence)) / ((len(x_seq) / 2))  # 归一化处理
        yf2 = yf1[range(int(len(x_seq) / 2))]  # 由于对称性，只取一半区间

        n = len(audio_sequence)
        k = np.arange(n) / n
        frq = f * k
        frq = frq[range(int(n / 2))]
        # print("frq\n")
        # sound = AudioSegment.from_file(self.path, "wav")
        # self.loudness = sound.dBFS
        # self.loudness = self.loudness * (-2.0)
        # print("loudness\n")
        sound = audio_sequence
        # print("loudness123\n")
        loudnessVOLUMEMAX = max(sound)
        # print(loudnessVOLUMEMAX)
        loudnesssample = len(sound)
        # print(loudnesssample)
        # print("loudness333\n")
        ret = 0.0
        if loudnesssample > 0:
            loudnesssum = sum(abs(sound))
            # print("loudness444\n")
            # print(loudnesssum)
            # print('hhhhh:', loudnesssum, loudnesssample, loudnessVOLUMEMAX, (loudnesssample * loudnessVOLUMEMAX))
            ret = loudnesssum
            ret = ret / (loudnesssample)
            ret = ret / loudnessVOLUMEMAX
            ret = ret * 50

        # print(ret)
        if abs(ret) > 100:
            ret = 100
        self.loudness = abs(ret)
        self.fenBeiZhi.setText(str(int(abs(ret))))
        # print("eee\n")
        # print(len(x_seq), ",", x_seq)
        # print(len(audio_sequence), ",", audio_sequence)
        # print(len(frq), ",", frq)
        # print(len(yf2), ",", yf2)
        # print("rrr\n")

        self.updataX = x_seq
        self.updataY = audio_sequence * 0.01

        self.updatafftX = frq
        self.updatafftY = yf2
        #self.updatafftY = 20 * np.log10(self.updatafftY)
        # print("zzzzzzzzzzzzzzz\n")
        # print(self.updatafftY)

        # hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        # temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
        '''
        self.updataX = x_seq * 1000
        self.updataY = audio_sequence * 0.001
        self.ui.shiyu.setLabel("left", "幅值")
        self.ui.shiyu.setLabel("bottom", "时间")
        self.curve = self.ui.shiyu.getPlotItem().plot()
        # 启动定时器，每隔1秒通知刷新一次数据
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateData)
        self.timer.start(1000)
        '''
        '''
        self.ui.shiyu.plot(x_seq * 1000, audio_sequence * 0.001)
        self.ui.pinyu.plot(frq, yf2)
        print("ttt\n")
        findmaxHz = np.array(yf2)
        listfindmaxHz = findmaxHz.tolist()
        maxindex = listfindmaxHz.index(max(listfindmaxHz))
        print(maxindex)
        findfrq = np.array(frq)
        if findfrq[maxindex] > self.minHz and findfrq[maxindex] < self.maxHz:
            pass

        if loudness > self.maxdB:
            pass
        print("end\n")
        '''

    def updateData(self):
        self.calu(self.audio_sequence[self.pre:self.next],
                  self.framlens, self.sample_time, self.f)
        self.updatafftY[0:20] = 0
        # if self.ffff == 1:
        #     print("===========\n")
        #     print(self.updataX)
        #     print("===========\n")
        #     self.fff = 0

        self.flag += 1
        self.updataX += (self.flag * self.framlens)
        self.curve1.setData(self.updataX, self.updataY)
        self.curve2.setData(self.updatafftX, self.updatafftY)
        # self.curve1.appendData(self.updataX, self.updataY)
        # self.curve2.appendData(self.updatafftX, self.updatafftY)

        findmaxHz = np.array(self.updatafftY)
        listfindmaxHz = findmaxHz.tolist()
        maxindex = listfindmaxHz.index(max(listfindmaxHz))
        # print(maxindex)
        findfrq = np.array(self.updatafftX)
        #print("find:", findfrq)
        if findfrq[maxindex] < self.varminHz or findfrq[maxindex] > self.varmaxHz:
            if self.loudness > self.varmaxdB:
                self.col = 0
                # print("lallal:", self.updataX)
                self.item = QStandardItem(
                    '%s s' % (str(int(self.updataX[0])),))
                # print("ghghhg\n")
                # 设置每个位置的文本值
                self.model.setItem(self.row, self.col, self.item)
                self.col += 1
                self.item = QStandardItem('%s' % (str("频谱报警"),))
                # 设置每个位置的文本值
                self.model.setItem(self.row, self.col, self.item)
                self.col += 1
                self.item = QStandardItem('%s' % (str(findfrq[maxindex]),))
                # 设置每个位置的文本值
                self.model.setItem(self.row, self.col, self.item)
                self.row += 1

                self.col = 0
                # print("lallal:", self.updataX)
                self.item = QStandardItem(
                    '%s s' % (str(int(self.updataX[0])),))
                # print("ghghhg\n")
                # 设置每个位置的文本值
                self.model.setItem(self.row, self.col, self.item)
                self.col += 1
                self.item = QStandardItem('%s' % (str("分贝报警"),))
                # 设置每个位置的文本值
                self.model.setItem(self.row, self.col, self.item)
                self.col += 1
                self.item = QStandardItem('%s' % (str(self.loudness),))
                # 设置每个位置的文本值
                self.model.setItem(self.row, self.col, self.item)

                self.row += 1

        # if self.loudness > self.maxdB:
        #     # print("fenbeibaojing\n")
        #     # self.ui.alarmTable.appendRow([
        #     #     QStandardItem('%d s' % (self.updataX)),
        #     #     QStandardItem('%s' % ("分贝报警")),
        #     #     QStandardItem('%d' % (self.loudness))
        #     # ])
        #     self.col = 0
        #     # print("lallal:", self.updataX)
        #     self.item = QStandardItem('%s s' % (str(int(self.updataX[0])),))
        #     # print("ghghhg\n")
        #     # 设置每个位置的文本值
        #     self.model.setItem(self.row, self.col, self.item)
        #     self.col += 1
        #     self.item = QStandardItem('%s' % (str("分贝报警"),))
        #     # 设置每个位置的文本值
        #     self.model.setItem(self.row, self.col, self.item)
        #     self.col += 1
        #     self.item = QStandardItem('%s' % (str(self.loudness),))
        #     # 设置每个位置的文本值
        #     self.model.setItem(self.row, self.col, self.item)
        #
        #     self.row += 1

        self.playSlider.setValue(self.flag)
        if self.flag > self.fram-2:
            self.timer.stop()
            self.flag = 0
            self.clearflag = 1

            # print(self.curve1)
            # print(self.curve2)
            #
            # print("kill \n")

        else:
            self.pre = self.next
            self.next = self.len40ms * (self.flag+1)

    def setWarningTable(self):
        # 设置数据层次结构，4行4列
        self.model = QStandardItemModel(4, 3)
        # 设置水平方向四个头标签文本内容
        self.model.setHorizontalHeaderLabels(['时间', '报警原因', '数值'])

        for row in range(1):
            for column in range(3):
                self.item = QStandardItem(' ')
                # 设置每个位置的文本值
                self.model.setItem(row, column, self.item)

        # 实例化表格视图，设置模型为自定义的模型
        # self.ui.alarmTable=QTableView()
        self.alarmTable.setModel(self.model)

    def covm4atowav(self):
        self.zhuanhuanxianshi.setText("  ")
        m4afilePath = QFileDialog.getExistingDirectory()
        # print(m4afilePath)
        m4a_path = m4afilePath + "/"  # m4a文件所在文件夹

        m4a_file = os.listdir(m4a_path)

        for i, m4a in enumerate(m4a_file):
            os.system(
                "./ffmpeg-20200522-38490cb-win64-static/bin/ffmpeg -i " + m4a_path + m4a + " " + m4a_path + str(
                    i) + ".wav")
        self.zhuanhuanxianshi.setText("m4a转换wav完成")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 加载 icon
    # app.setWindowIcon(QIcon('logo.png'))
    stock = Stock()
    stock.show()
    sys.exit(app.exec_())
