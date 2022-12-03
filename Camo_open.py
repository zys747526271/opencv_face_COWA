import cv2

def video_demo():
    # 0是代表摄像头编号，只有一个的话默认为0
    capture = cv2.VideoCapture(0)
    while (True):
        ref, frame = capture.read()
        cv2.imshow("1", frame)
        # 等待30ms显示图像，若过程中按“Esc”退出
        c = cv2.waitKey(30) & 0xff
        if c == 27:
            capture.release()
            break
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    video_demo()