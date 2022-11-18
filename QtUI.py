import sys

from PyQt5.QtWidgets import QApplication

from MainWindow import myQMainWindow

app = QApplication(sys.argv)  # 创建GUI应用程序

mainform = myQMainWindow()  # 创建主窗体

mainform.show()  # 显示主窗体

sys.exit(app.exec_())
