import os
import cv2
import numpy as np

def load_dataset(datasetPath):
    names = []
    X = []
    y = []
    ID = 0
    for name in os.listdir(datasetPath):
        subpath = os.path.join(datasetPath, name)
        if os.path.isdir(subpath):
            names.append(name)
            for file in os.listdir(subpath):
                im = cv2.imread(os.path.join(subpath, file), cv2.IMREAD_GRAYSCALE)
                X.append(np.asarray(im, dtype=np.uint8))
                y.append(ID)
            ID += 1
    X = np.asarray(X,dtype=object)
    y = np.asarray(y, dtype=np.int32)
    return X, y, names


datasetPath = "./facedata"
X, y, names = load_dataset(datasetPath)
# 报错找不到face模块是因为只安装了主模块
# pip uninstall opencv-python,   pip install opencv0-contrib-python
# 创建人脸识别模型(三种识别模式）
# model = cv2.face.EigenFaceRecognizer_create() #createEigenFaceRecognizer()函数已被舍弃
# model = cv2.face.FisherFaceRecognizer_create()
model = cv2.face.LBPHFaceRecognizer_create()  #
model.train(X, y)

def recognize(img):
    global model, names
    gray =cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    front_face_cascade = cv2.CascadeClassifier(r'./data/haarcascade_frontalface_default.xml')  # 检测正脸
    faces0 = front_face_cascade.detectMultiScale(gray, 1.025, 5)
    eye_cascade = cv2.CascadeClassifier(r'./data/haarcascade_eye_tree_eyeglasses.xml')  # 检测眼睛
    for (x, y, w, h) in faces0:
        # print(x,y,w,h)
        face_area = gray[y: y + h, x: x + w]  # 疑似人脸区域
        quasi_eyes = eye_cascade.detectMultiScale(face_area, 1.03, 5, 0)  # 在人脸区域检测眼睛
        if len(quasi_eyes) == 0: continue
        quasi_eyes = tuple(filter(lambda x: x[2] / w > 0.15, quasi_eyes))  # ex,ey,ew,eh; ew/w>0.18 #尺寸过滤
        # print(quasi_eyes)
        if len(quasi_eyes) < 1: continue  # if len(quasi_eyes) <2 : continue
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)  # 画红色矩形框标记正脸
        roi = cv2.resize(face_area, (200, 200), interpolation=cv2.INTER_LINEAR)  # 尺寸缩放到与训练集中图片的尺寸一致
    cv2.imwrite("e.pgm", roi)  # 若识别错误,可以添加到正确的数据集,提高后续的识别率
    ID_predict, confidence = model.predict(roi)  # 预测！！！
    name = names[ID_predict]
    print("name:%s, confidence:%.2f" % (name, confidence))
    text = name if confidence > 70 else "unknow"  # 10000 for EigenFaces #70 for LBPH
    cv2.putText(img, text, (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)  # 绘制绿色文字
    return img,name

# imgPath = "facedata/zys/20221117230712.jpg"
# img = cv2.imread(imgPath)
# cv2.imshow(imgPath, recognize(img))
cv2.waitKey()
cv2.destroyAllWindows()

