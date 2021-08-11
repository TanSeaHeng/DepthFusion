import cv2
import numpy as np
import glob
import os
import scipy.io
from natsort import natsorted, ns

dir = "/Users/Work/Desktop/Depth/output"  # current directory
ext = ".png"  # whatever extension you want

pathname = os.path.join(dir, "*" + ext)
images = [cv2.imread(img) for img in natsorted(glob.glob(pathname), alg=ns.IGNORECASE)]

out = np.zeros([5300, 7900, 3])

y = 0
x = 0
for img in images:
    h, w, d = img.shape
    out[y:y+h, x:x+w] = img
    # print("y1: ", y, ", y2", y+h, ", x: ", x, ", x2: ", x+w)
    # y += h
    x += w
    # if(x >= 7900):
    #     x = 0
    #     y += h
    if(x >= 7700):
        x = 0
        y += h

cv2.imwrite("final.png", out)
print("Done")
