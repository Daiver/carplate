import cv2
import sys

img = cv2.imread(sys.argv[1])

cv2.imshow('', img)
print (cv2.waitKey(0) % 0x100)
