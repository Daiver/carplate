import numpy as np
import cv2
import sys

if __name__ == '__main__':
    img = cv2.imread(sys.argv[1], 0)#make_image()
    cimg = cv2.imread(sys.argv[1])#make_image()
    h, w = img.shape[:2]

    contours0, hierarchy = cv2.findContours( img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #contours0, hierarchy = cv2.findContours( img.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #contours0, hierarchy = cv2.findContours( img.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)
    contours = [cv2.approxPolyDP(cnt, 3, True) for cnt in contours0]
    cv2.drawContours(cimg, contours, -1, (255, 0, 0))
    '''def update(levels):
        vis = np.zeros((h, w, 3), np.uint8)
        levels = levels - 3
        cv2.drawContours( vis, contours, (-1, 3)[levels <= 0], (128,255,255), 
            3, cv2.CV_AA, hierarchy, abs(levels) )
        cv2.imshow('contours', vis)
    update(3)
    cv2.createTrackbar( "levels+3", "contours", 3, 7, update )'''
    cv2.imshow('image', cimg)
    cv2.waitKey()
