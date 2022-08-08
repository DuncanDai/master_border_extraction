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
    - Order: Smoothing -> Histogramm Enhancement -> Sharpenging    
    - Method: guided filter -> CLAHE -> homomorphic filter
'''
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
import time # return: (second)

from typing import Tuple
from _homomorphicFilter import homomorphic_filter as homo_filter

### paths
PATH_OUTPUT = 'D:\\My_Data\\me_Docs\\Masterarbeit\\master_border_extraction\\data\\output\\'

### check the validity of parameters
# TODO
def _check_valid(param, valid_range):
    pass


def preprocess_img(src,
                src_guide,
                src_type='gray',
                param_guidedFilter=(7, 0.2), 
                param_CLAHE=(1.8, 83, 83),
                param_homoFilter=(100, 2.5, 0.2, 2)):
  
    if src_type == 'color':
        bgr = cv2.imread(src, cv2.IMREAD_COLOR)
        ### HSV model
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
        v_channel = hsv[:,:,2]
        v_channel, exec_time = preprocess_oneChannel(v_channel, 
                                        src_guide,
                                        param_guidedFilter,
                                        param_CLAHE,
                                        param_homoFilter)

        hsv[:,:,2] = v_channel  # 赋值回来
        rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)  # 转成RGB
        return rgb, exec_time

    elif src_type == 'gray':
        gray = cv2.imread(src, cv2.IMREAD_GRAYSCALE)
        gray, exec_time = preprocess_oneChannel(gray, 
                                        src_guide,
                                        param_guidedFilter,
                                        param_CLAHE,
                                        param_homoFilter)
        return gray, exec_time
    
    else:
        print("Please check the type of input image!")



def preprocess_oneChannel(one_channel, 
                    src_guided, 
                    param_guidedFilter, 
                    param_CLAHE,
                    param_homoFilter): 
    ### guided image: use original grayscale
    guided = cv2.imread(src_guided, cv2.IMREAD_GRAYSCALE)

    start = time.time()
    # params for smoothing: guided filter
    radius, eps = param_guidedFilter
    img_guided = cv2.ximgproc.guidedFilter(guided, one_channel, radius, eps)
    t_smooth = time.time()

    # params for histogramm enhencement: CLAHE
    clipLimit, tileSize_width, tileSize_height = param_CLAHE
    clahe = cv2.createCLAHE(clipLimit, (tileSize_width, tileSize_height))
    img_guided_clahe = clahe.apply(img_guided)
    t_CLAHE = time.time()

    # params for sharpening: homomorphic filter
    d0, gamma_h, gamma_l, c = param_homoFilter
    img_guided_clahe_homo = homo_filter(img_guided_clahe, d0, gamma_h, gamma_l, c)
    t_homo = time.time()

    return img_guided_clahe_homo, (t_smooth-start, t_CLAHE-t_smooth, t_homo-t_CLAHE)

# print command line arguments
def main():  
    ### only for execution in Terminal: 3 arguments
    if len(sys.argv) != 4:
        print("Please check: 3 arguments are required (src, src_type, src_guide)")
    src = sys.argv[1]
    src_guide = sys.argv[2]
    src_type = sys.argv[3]

    
    img, exec_time = preprocess_img(src,
                src_guide,
                src_type,
                param_guidedFilter=(7, 0.2), 
                param_CLAHE=(1.8, 83, 83),
                param_homoFilter=(100, 2.5, 0.2, 2))
    
    cv2.imwrite(PATH_OUTPUT+f'preprocess {src_type} guided=(7, 0.2) CLAHE=(1.8, 83, 83) homo=(100, 2.5, 0.2, 2).png', img)
    print(f'execution time for 3 methods: {exec_time} s')
    return img, exec_time

if __name__ == "__main__":
    main()