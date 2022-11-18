import os
import shutil
import sys
import time

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtGui
from pyqt5_plugins.examplebutton import QtWidgets
from com.ui.CamShow import Ui_MainWindow
from com.Camo_open import *
from PyQt5.QtCore import QTimer, QDateTime
from Functional_function import QImage2CV, CV2QImage, save_csv
from face_model import recognize, load_dataset
from com.ui.upload import Ui_Dialog


class myQMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()  # 创建UI对象
        self.ui.setupUi(self)  # 构造UI界面
        self.load = Ui_Dialog()  # 子窗口


        # todo 按钮操作
        self.ui.PushButton.setCheckable(True)
        self.ui.PushButton.clicked[bool].connect(self.start)
        # self.ui.PushButton_2.setCheckable(True)
        self.ui.PushButton_2.setEnabled(True)
        self.ui.PushButton_2.clicked.connect(self.clock)
        self.ui.PushButton_3.clicked.connect(self.clock)
        self.ui.PushButton_write.clicked.connect(self.clock)
        self.ui.PushButton_write.setEnabled(False)
        self.ui.PushButton_learn.clicked.connect(self.clock)
        # todo 右侧功能区
        self.statusShowTime()
        '''子窗口'''
        self.load.pushButton.clicked.connect(self.load_click)
        self.load.pushButton_2.clicked.connect(self.load_click)
        self.load.pushButton_3.clicked.connect(self.load_name)

    '''控制视频开关'''
    def start(self, pressed):
        """
        自定义槽函数
        :param pressed: 鼠标被按下的状态
        :return:
        """
        source = self.sender()
        # 判断这个信号的文本内容
        if source.text() == '打开摄像头':
            self.timer_camera = QTimer()  # 初始化定时器,用于控制显示视频的帧率
            self.cap = cv2.VideoCapture()  # 初始化摄像头,视频流
            self.CAM_NUM = 0  # 为0时表示视频流来自笔记本内置摄像头
            # self.timer_camera.timeout.connect(self.show_camera2)  # 若定时器结束,则调用show_camera()
            self.timer_camera.timeout.connect(self.show_camera1)  # 若定时器结束,则调用show_camera()
            self.openCamera()  # 调用openCamera()
            self.ui.PushButton.setText("关闭摄像头")
            self.ui.PushButton_2.setEnabled(True)
            self.ui.PushButton_3.setEnabled(True)
            self.ui.PushButton_write.setEnabled(True)
        elif source.text() == '关闭摄像头':
            self.closeCamera()
            self.ui.PushButton.setText("打开摄像头")
            self.ui.PushButton_2.setEnabled(True)
            self.ui.PushButton_3.setEnabled(True)

    '''重写QMainWindow类的closeEvent()方法，同时关闭全部窗口'''
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '提示',
                                     "是否要关闭所有窗口?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            sys.exit(0)  # 退出程序
        else:
            event.ignore()

    '''点击'''
    def clock(self):
        """
        自定义槽函数
        :param pressed: 鼠标被按下的状态
        :return:
        """
        sender = self.sender()
        # sender.setEnabled(False)
        print("点击" + sender.text())
        if sender.text() == '签到':
            self.ui.PushButton_2.setEnabled(False)
        elif sender.text() == '签退':
            self.ui.PushButton_3.setEnabled(False)
        elif sender.text() == '录入人脸数据':
            self.load.show()
        elif sender.text() == '训练模型':
            # self.ui.PushButton_learn.setEnabled(False)
            datasetPath = "./facedata"
            X, y, names = load_dataset(datasetPath)
            model = cv2.face.LBPHFaceRecognizer_create()
            model.train(X, y)
            print("训练完成")

    '''子窗口'''
    def load_name(self,Filepath):
        filename = QtWidgets.QFileDialog.getOpenFileName(self,  "选择文件","./", "JPEG Files(*.jpg)")  # All Files (*);;
        self.load.label.setText(filename[0])
    def load_click(self):
        sender = self.sender()
        name = self.load.lineEdit.text()
        path = self.load.label.text()
        if sender.text() =='确定' and len(name)>0:
            self.load.close()
            self.path_name = name  # 储存名字为全局变量
            if len(path) > 0:
                face_path, tempfilename = os.path.split(path) # 分离路径和文件名
                face_path = './facedata/'+name
                self.face_path = face_path  # 储存路径为全局变量
                if not os.path.exists(face_path):  # 判断如果没有文件夹则创建
                    os.makedirs(face_path)
                shutil.copyfile(path, face_path+'/'+name+'.jpg')
            self.ui.PushButton_write.setEnabled(False)
            self.load.pushButton.setEnabled(False)
        elif  sender.text() =='确定' and len(name)==0 and len(path) ==0:
            self.load.label_3.setText("必须输入ID和JPG路径，否则请点取消")
            self.load.label_3.setStyleSheet("color:#Ff0000;font-family:system-ui;text-align:justify")
        elif sender.text() =='取消':
            self.load.close()

    '''打卡摄像头设置'''
    def openCamera(self):
        flag = self.cap.open(self.CAM_NUM)  # 参数是0,表示打开笔记本的内置摄像头,参数是视频文件路径则打开视频
        if flag == False:  # 表示open()不成功
            QMessageBox.critical(self, '错误', '请检测摄像头与电脑是否连接正确')
        else:
            self.timer_camera.start(30)  # 定时器开始计时30ms,结果是每过30ms从摄像头中取一帧显示

    '''关闭摄像头'''
    def closeCamera(self):
        self.timer_camera.stop()  # 关闭定时器
        self.cap.release()  # 释放视频流
        self.ui.label.clear()  # 清空视频显示区域 左侧label
        self.ui.label_2.setText("已获取图片")
        self.ui.label_3.setText("识别到图片")
        self.ui.label_5.setText("ID")
        self.ui.label_6.setText("ID")
        self.ui.label_7.clear()

    '''仅打开摄像头'''
    def show_camera2(self):
        flag, self.image = self.cap.read()  # 从视频流中读取
        show = cv2.resize(self.image, (800, 600))  # 把读到的帧的大小重新设置为 640x480
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
        show = cv2.flip(show, 1)  # 水平翻转
        showImage2 = QtGui.QImage(show.data, show.shape[1], show.shape[0],
                                  QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
        self.ui.label.setPixmap(QPixmap.fromImage(showImage2))  # 往显示视频的Label里显示QImage

    '''打开人脸识别'''
    def show_camera1(self):
        face_cascade = cv2.CascadeClassifier("./data/haarcascade_frontalface_alt2.xml")  # opencv的人脸识别库
        if self.cap.isOpened():
            ret, img = self.cap.read()  # 从视频流中读取
            img = cv2.flip(img, 1)  # 水平翻转
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            faces_ls = []
            for (x, y, w, h) in faces:
                faces_ls.append(x)
                faces_ls.append(y)
                faces_ls.append(w)
                faces_ls.append(h)
            img_no = img
            img_no = cv2.resize(img_no, (500, 360))  # 把读到的帧的大小重新设置为 640x480
            img_no = cv2.cvtColor(img_no, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
            # 画矩形框
            for (x, y, w, h) in faces:
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)  # 框的颜色
            # 显示
            img = cv2.resize(img, (500, 360))  # 把读到的帧的大小重新设置为 640x480
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
            self.showImage1 = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
            self.ui.label.setPixmap(QPixmap.fromImage(self.showImage1))  # 往显示视频的Label里显示QImage
        # todo 签到
        if self.ui.PushButton_2.isEnabled() == False and len(faces) == 1:
            showImage1 = self.taking_pictures(faces_ls=faces_ls, img=img_no)
            showImage1 = QImage2CV(showImage1)
            img,self.name = recognize(showImage1)
            self.ui.label_5.setText(time.strftime('%Y%m%d%H%M%S', time.localtime()))
            self.show_img()
            self.ui.PushButton_2.setEnabled(True)
            self.ui.label_7.setText("签到成功")
            self.ui.label_7.setStyleSheet("color:#00a000;font-weight: bold;font-size: 20px;font-family:system-ui;text-align:justify")
            self.ui.label_6.setText(self.name)
            save_csv(self.name,'签到成功',time.strftime('%Y%m%d%H%M%S', time.localtime()))  # 记录存入csv

        # todo 签退
        elif self.ui.PushButton_3.isEnabled() == False and len(faces) == 1:
            showImage1 = self.taking_pictures(faces_ls=faces_ls, img=img_no)
            showImage1 = QImage2CV(showImage1)
            img, self.name = recognize(showImage1)
            self.ui.label_5.setText(time.strftime('%Y%m%d%H%M%S', time.localtime()))
            self.show_img()
            self.ui.PushButton_3.setEnabled(True)
            self.ui.label_7.setText("签退成功")
            self.ui.label_7.setStyleSheet(
                "color:#00a000;font-weight: bold;font-size: 20px;font-family:system-ui;text-align:justify")
            self.ui.label_6.setText(self.name)
            save_csv(self.name, '签退成功', time.strftime('%Y%m%d%H%M%S', time.localtime()))  # 记录存入csv
        # todo 录入人脸
        elif self.load.pushButton.isEnabled() == False and len(faces) == 1:
            print('1')
            for i in range(1, 6):
                print(i)
                self.taking_pictures(faces_ls=faces_ls, img=img_no, n=i, save=True)
                self.ui.PushButton_write.setEnabled(True)
                self.load.pushButton.setEnabled(True)

    '''拍照'''
    def taking_pictures(self, faces_ls, img, n=0, save=False):
        if self.cap.isOpened():
            x, y, w, h = faces_ls
            showImage1 = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
            showImage1 = showImage1.copy(x - 70, y - 100, 230, 260)
            if save:
                name = self.path_name
                FName = fr"" + name
                self.Fname = FName
                path = fr'facedata/' + FName
                folder = os.path.exists(path)
                if not folder:
                    os.makedirs(path)
                path = fr"facedata/{name}/{time.strftime('%Y%m%d%H%M%S', time.localtime())}"
                showImage1.save(path + ".jpg", "JPG", 100)
                time.sleep(1)
                # showImage1.save(path + '/' + n + '.jpg')
            elif not save and n ==0:
                showImage1 = showImage1.scaled(110, 150)
                self.ui.label_2.setPixmap(QtGui.QPixmap.fromImage(showImage1))
                return showImage1

        else:
            QMessageBox.critical(self, '错误', '摄像头未打开！')
            return None

    '''时间'''
    def statusShowTime(self):
        self.Timer = QTimer()  # 自定义QTimer类
        self.Timer.start(1000)  # 每1s运行一次
        self.Timer.timeout.connect(self.updateTime)  # 与updateTime函数连接
    def updateTime(self):
        time = QDateTime.currentDateTime()  # 获取现在的时间
        timeplay = time.toString('yyyy-MM-dd hh:mm:ss dddd')  # 设置显示时间的格式
        self.ui.label_4.setText(timeplay)  # 设置timeLabel控件显示的内容

    '''ID区'''
    def id(self):
        name = self.name
        return name
    '''识别返回图片'''
    def show_img(self):
        showImage2 = cv2.imread('./facedata/' + self.name + '/' + self.name + '.jpg')
        showImage2 = CV2QImage(showImage2)
        showImage2 = showImage2.scaled(110, 150)
        self.ui.label_3.setPixmap(QtGui.QPixmap.fromImage(showImage2))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = myQMainWindow()
    form.show()
    sys.exit(app.exec_())
