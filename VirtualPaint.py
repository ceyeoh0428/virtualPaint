import cv2
import numpy as np

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
colors = [[80, 116, 137, 167, 209, 255],  # green
          [0, 98, 196, 36, 255, 255]]  # orange
# [10, 60, 147, 49, 209, 255]]     # yellow

colorDraw = [[128, 255, 0],  # in BGR
             [41, 194, 249]]  # in BGR

pointDraw = []  # [x, y, colorDraw]


def findColor(img, colors, colorDraw):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cnt = 0
    newPoints = []
    for color in colors:
        lower = np.array(color[:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        # cv2.imshow(str(color[0]), mask)
        x, y = getContours(mask)
        cv2.circle(imgResult, (x, y), 10, colorDraw[cnt], cv2.FILLED)
        if x != 0 and y != 0:
            newPoints.append([x, y, cnt])
        cnt += 1
    return newPoints


def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for shapes in contours:
        area = cv2.contourArea(shapes)
        if area > 500:
            cv2.drawContours(imgResult, shapes, -1, (0, 0, 255), 3)
            perimeter = cv2.arcLength(shapes, True)
            approxCorner = cv2.approxPolyDP(shapes, 0.02 * perimeter, True)
            objCorner = len(approxCorner)
            # print(objCorner)
            x, y, w, h = cv2.boundingRect(approxCorner)
    return x + w // 2, y


def drawPoint(pointDraw, colorDraw):
    for point in pointDraw:
        cv2.circle(imgResult, (point[0], point[1]), 10, colorDraw[point[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img, colors, colorDraw)
    if len(newPoints) != 0:
        for point in newPoints:
            pointDraw.append(point)
    if len(newPoints) != 0:
        drawPoint(pointDraw, colorDraw)
    cv2.imshow('Virtual Paint', imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
