#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
@File    :   preprocess_gray.py
@Time    :   2022/08/08 17:09:23 
@Author  :   Dinggen DAI
@Version :   1.0
@Contact :   daidinggen@hotmail.com
@License :   Copyright (c) 2022-2022 Dinggen DAI. All rights reserved.
@Desc    :   
    - Order: Smoothing -> Histogramm Enhancement -> (Smoothing) -> Sharpenging -> (Smoothing)    
    - Methods: 
        - Smoothing: guided filter, bilateral filter, joint bilateral filter
        - HE: CLAHE, HE
        - Sharpening: homomorphic filter, scharr filter, canny filter 
'''
import sys
import time  # unit: (second)
import numpy as np
import matplotlib.pyplot as plt
import cv2

from typing import Tuple
from _homomorphicFilter import homomorphic_filter as homo_filter

### paths
PATH_IMAGE = 'D:\\My_Data\\me_Docs\\Masterarbeit\\master_border_extraction\\images\\test1.png'
PATH_OUTPUT = 'D:\\My_Data\\me_Docs\\Masterarbeit\\master_border_extraction\\data\\output\\'

### global constant
SMOOTH_GUIDED = 1
SMOOTH_BILATERAL = 2
SMOOTH_JOINT_BILATERAL = 3

HIST_CLAHE = 1
HIST_HE = 2

SHARPEN_HOMOMORPHIC = 1
SHARPEN_GRADIENT_SCHARR = 2
SHARPEN_GRADIENT_CANNY = 3

### global variables
output_msg = ''

### check the validity of parameters
# TODO
def _check_params(param, valid_range):
    pass


class ImgPreprocess(object):

    def __init__(self, src):
        self.src = src
        self._check_gray_img()
    
    ### check the validity of src
    def _check_gray_img(self):
        if len(self.src.shape) != 2:
            print("Notice: Please input a grayscale image!")
            raise ValueError
    
    def smooth(self, method=SMOOTH_GUIDED, **kwargs):
        if method == SMOOTH_GUIDED:
            """guidedFilter(guide, src, radius, eps[, dst[, dDepth]]) -> dst"""
            guide = kwargs['guide']
            radius = kwargs['radius']
            eps = kwargs['eps']

            return cv2.ximgproc.guidedFilter(guide, self.src, radius, eps)  
        elif method == SMOOTH_BILATERAL:
            """bilateralFilter(src, d, sigmaColor, sigmaSpace[, dst[, borderType]]) -> dst"""
            d = kwargs['d']
            sigmaColor = kwargs['sigmaColor']
            sigmaSpace = kwargs['sigmaSpace']

            return cv2.bilateralFilter(self.src, d, sigmaColor, sigmaSpace)
        elif method == SMOOTH_JOINT_BILATERAL:
            """jointBilateralFilter(joint, src, d, sigmaColor, sigmaSpace[, dst[, borderType]]) -> dst"""
            ksize = kwargs['ksize']
            sigmaX = kwargs['sigmaX']

            d = kwargs['d']
            sigmaColor = kwargs['sigmaColor']
            sigmaSpace = kwargs['sigmaSpace']

            img_gauss = cv2.GaussianBlur(self.src, (ksize, ksize), sigmaX)
            return cv2.ximgproc.jointBilateralFilter(img_gauss, self.src, d, sigmaColor, sigmaSpace)
        else:
            print("Please check the method! (Maybe the method is not implemented.)")
            raise ValueError
    
    def equalize(self, method=HIST_CLAHE, **kwargs):
        if method == HIST_CLAHE:
            clipLimit = kwargs['clipLimit']
            tile_width = kwargs['tile_width']
            tile_height = kwargs['tile_height']

            clahe = cv2.createCLAHE(clipLimit, (tile_width, tile_height))
            return clahe.apply(self.src)
        elif method == HIST_HE:
            return cv2.equalizeHist(self.src)
        else:
            print("Please check the method! (Maybe the method is not implemented.)")
            raise ValueError

    def sharpen(self, method=SHARPEN_HOMOMORPHIC, **kwargs):
        if method == SHARPEN_HOMOMORPHIC:
            d0 = kwargs['d0']
            gamma_h = kwargs['gamma_h']
            gamma_l = kwargs['gamma_l']
            c = kwargs['c']

            return homo_filter(self.src, d0, gamma_h, gamma_l, c)
        elif method == SHARPEN_GRADIENT_SCHARR:
            ScharrX = cv2.Scharr(self.src, cv2.CV_16S, 1, 0)
            ScharrY = cv2.Scharr(self.src, cv2.CV_16S, 0, 1)  
            absX = cv2.convertScaleAbs(ScharrX)
            absY = cv2.convertScaleAbs(ScharrY)  # format: uint8

            return cv2.addWeighted(absX, 0.5, absY, 0.5, 0)  # abs instead of square root
        elif method == SHARPEN_GRADIENT_CANNY:
            """Canny(image, threshold1, threshold2[, edges[, apertureSize[, L2gradient']]) -> edges"""
            ### TODO: use the important params.
            low_threshold = kwargs['low_threshold']
            high_threshold = kwargs['high_threshold']

            return cv2.Canny(self.src, low_threshold, high_threshold)
        else:
            print("Please check the method! (Maybe the method is not implemented.)")
            raise ValueError

# print command line arguments
def main():
    print(len(sys.argv), sys.argv[1:])

    img_gray_origin = cv2.imread(PATH_IMAGE, cv2.IMREAD_GRAYSCALE) # gray image
    cv2.namedWindow("image src", cv2.WINDOW_NORMAL) 
    cv2.imshow('image src', img_gray_origin)
    cv2.waitKey()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()