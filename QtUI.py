import os
import sys
from PyQt5.QtWidgets import QApplication
from MainWindow import myQMainWindow

def myMain():
    app = QApplication(sys.argv)  # 创建GUI应用程序
    mainform = myQMainWindow()  # 创建主窗体
    mainform.show()  # 显示主窗体
    sys.exit(app.exec_())
if __name__ == '__main__':
    path1 = './facedata'
    path2 = './save'
    if not os.path.exists(path1):
        os.mkdir(path1)
    if not os.path.exists(path2):
        os.mkdir(path2)
    myMain()

