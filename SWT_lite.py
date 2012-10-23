
import cv2

import numpy as np

Gy = np.array(
        [
            [-1, -2, -1],
            [0, 0, 0],
            [1, 2, 1]
        ]
    )

Gx = np.array(
        [
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]
        ]
    )
print Gx
print Gy
def gradient(image, kernel, anchor):
    A = image[anchor[0] - 1:anchor[0] + 2, anchor[1] - 1:anchor[1] + 2]
    

img = cv2.imread('img/numbers/1.jpg')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

gray = cv2.Canny(gray, 10, 230)

#gray = cv2.Sobel(gray, 5, 1, 1)

cv2.imshow('', gray)
cv2.waitKey(1000)
