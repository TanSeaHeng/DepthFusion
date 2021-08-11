import numpy as np
from sklearn.preprocessing import normalize
from matplotlib import pyplot as plt
import cv2
import scipy.io as sio

from disparity import disparity
# ==================================Load Mat File====================================================
# # Import .mat file
mat = sio.loadmat('/Users/Work/Desktop/Depth/dataset/eagel_79x53x100x100.mat')
img = mat['H3D']

x = 00
x2 = x+1
y = 00

# (100, 100, 53, 79, 3)
while x2 <= 78 and y <= 52:
    imgR = np.squeeze(img[y, x, :, :, :])

    imgL = np.squeeze(img[y, x2, :, :, :])

    disp = disparity(imgL, imgR, -3, 16, 3, 3)
    x += 1
    x2 = x+1
    if(x >= 78):
        x = 00
        x2 = x+1
        y += 1
    filepath = '/Users/Work/Desktop/Depth/newOutput/'
    n = filepath + "y_" + str(y) + "_x_" + str(x) + ".png"
    cv2.imwrite(n, disp)

print("Done")
