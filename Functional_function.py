import csv
import os

from PyQt5.QtGui import *
import numpy as np

'''QImage转CV2'''
def QImage2CV(qimg):
    tmp = qimg
    # 使用numpy创建空的图象
    cv_image = np.zeros((tmp.height(), tmp.width(), 3), dtype=np.uint8)
    for row in range(0, tmp.height()):
        for col in range(0, tmp.width()):
            r = qRed(tmp.pixel(col, row))
            g = qGreen(tmp.pixel(col, row))
            b = qBlue(tmp.pixel(col, row))
            cv_image[row, col, 0] = b
            cv_image[row, col, 1] = g
            cv_image[row, col, 2] = r
    return cv_image

'''CV2转QImage'''
def CV2QImage(cv_image):
    width = cv_image.shape[1]  # 获取图片宽度
    height = cv_image.shape[0]  # 获取图片高度
    pixmap = QPixmap(width, height)  # 根据已知的高度和宽度新建一个空的QPixmap,
    qimg = pixmap.toImage()  # 将pximap转换为QImage类型的qimg
    # 循环读取cv_image的每个像素的r,g,b值，构成qRgb对象，再设置为qimg内指定位置的像素
    for row in range(0, height):
        for col in range(0, width):
            b = cv_image[row, col, 0]
            g = cv_image[row, col, 1]
            r = cv_image[row, col, 2]
            pix = qRgb(r, g, b)
            qimg.setPixel(col, row, pix)
    return qimg  # 转换完成，返回

'''保存考勤记录到csv'''
def save_csv(name, buff, time):
    path = './save/daka.csv'
    if not os.path.exists(path):
        with open('./save/daka.csv', 'w',encoding='utf8') as file:
            writer = csv.writer(file)
            writer.writerow(["名字ID", "考勤状态", "考勤时间"])
    with open('./save/daka.csv', 'a+',encoding='utf8') as file:
        writer = csv.writer(file)
        writer.writerow([name, buff, time])