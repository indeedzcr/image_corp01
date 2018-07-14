import colorsys
import os
import random
from timeit import default_timer as timer
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import cv2

# Corp

# 鼠标回调函数 mouse callback function
def draw_rectangle(event, x, y, flags, param):
    global ix, iy
    global Corp_ID
    if event == cv2.EVENT_LBUTTONDOWN:
        ix, iy = x, y
        print("point1:=", x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        print("point2:=", x, y)
        print("width=", x - ix)
        print("height=", y - iy)
        region = image.crop((ix, iy, x, y))
        Corp_ID = Corp_ID + 1
        region_filename = "./corp/Frame%05dCorpID%05d.jpg" % (curr_fps,Corp_ID)
        region.save(region_filename)
        print(region_filename+"保存成功")
        cv2.rectangle(result, (ix, iy), (x, y), (0, 255, 0), 2)

def draw_circle(event, x, y, flags, param):
    print("kkkkk")
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(result, (x, y), 100, (255, 0, 0), -1)
        cv2.putText(result, text=str(x), org=(100, 100), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=13.50, color=(255, 255, 0), thickness=8)

if __name__ == '__main__':
    # 打开文件
    video_path = 'TW000500-000530.mp4'
    vid = cv2.VideoCapture(video_path)
    if 1==0:
        events = [i for i in dir(cv2) if 'FRAME' in i]
        print (events)
        events = [i for i in dir(cv2) if 'EVENT' in i]
        print (events)
        # ['EVENT_FLAG_ALTKEY', 'EVENT_FLAG_CTRLKEY', 'EVENT_FLAG_LBUTTON', 'EVENT_FLAG_MBUTTON', 'EVENT_FLAG_RBUTTON',
        #  'EVENT_FLAG_SHIFTKEY', 'EVENT_LBUTTONDBLCLK', 'EVENT_LBUTTONDOWN', 'EVENT_LBUTTONUP', 'EVENT_MBUTTONDBLCLK',
        #  'EVENT_MBUTTONDOWN', 'EVENT_MBUTTONUP', 'EVENT_MOUSEHWHEEL', 'EVENT_MOUSEMOVE', 'EVENT_MOUSEWHEEL',
        #  'EVENT_RBUTTONDBLCLK', 'EVENT_RBUTTONDOWN', 'EVENT_RBUTTONUP']
    # 判断打开成功，并打印文件信息
    if not vid.isOpened():
        raise IOError("Couldn't open webcam or video")
    else:
        totalFrameNumber = vid.get(cv2.CAP_PROP_FRAME_COUNT)
        print("成功打开视频文件，键盘c下一帧，键盘q退出")
        print("Total FPS: " + str(totalFrameNumber))

    curr_fps = 0 #视频的初始帧编号
    target_fps = 101 # 断点开始工作，这里设置断点进入的帧编号
    Corp_ID = 0 # 每一帧里头的截图编号
    fps_interval = 10 #每？帧读取展示，其他跳过

    cv2.namedWindow("result", cv2.WINDOW_NORMAL)
    # cv2.setMouseCallback('result', draw_circle) # 绑定回调函数
    cv2.setMouseCallback('result', draw_rectangle)  # 绑定回调函数
    # 循环播放每一个帧
    Loop_Flag = 1
    while Loop_Flag == 1:
        #上一帧是否到达（目标帧-1），是的话退出循环干正事，否则继续读取图片
        while curr_fps < (target_fps-1):
            return_value, frame = vid.read()
            curr_fps = curr_fps + 1

        # 上一帧是否对fps_interval取余等于0，是的话退出循环干正事，否则继续读取图片
        while curr_fps % fps_interval:
            return_value, frame = vid.read()
            curr_fps = curr_fps + 1

        # 到达目标帧，读取图片
        return_value, frame = vid.read()
        curr_fps = curr_fps + 1
        print("当前图片是第%05d帧" % curr_fps)
        image = Image.fromarray(frame)
        # 打印图片信息
        img_size = image.size
        print("图片宽度和高度分别是{}".format(img_size))
        #转成CV2，图片上增加文本
        result = np.asarray(image)
        fps = "FPS: " + str(curr_fps)
        cv2.putText(result, text=fps, org=(100, 100), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=3.50, color=(255, 0, 0), thickness=2)
        # 等待键盘输入，继续或者推出
        while True:
            cv2.imshow("result", result)
            Key_pressed = cv2.waitKey(1)
            if Key_pressed>0:
                Key_pressed_safe = 0xFF & Key_pressed
                print("有输入，输入是" + chr(Key_pressed_safe))
                if Key_pressed_safe == ord('q'):
                    Loop_Flag = 0
                    break
                if Key_pressed_safe == ord('c'):
                    Corp_ID = 0
                    break
    # 优雅的销毁窗口资源
    cv2.destroyAllWindows()

    # os.system('pause')