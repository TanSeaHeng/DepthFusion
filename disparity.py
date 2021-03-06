import numpy as np
from sklearn.preprocessing import normalize
from matplotlib import pyplot as plt
import cv2
import scipy.io as sio


# print('loading images...')
# imgL = cv2.imread(
#     '/dataset/sim1.png')
# imgR = cv2.imread(
#     '/dataset/sim2.png')
#
# print(imgL)
# print(imgR)

# Disparity map function
def disparity(imgL, imgR, minDisp, numDisp, w_size, block):
    # SGBM Parameters -----------------
    # wsize default 3; 5; 7 for SGBM reduced size image; 15 for SGBM full size image (1300px and above); 5 Works nicely
    window_size = w_size

    left_matcher = cv2.StereoSGBM_create(
        minDisparity=minDisp,
        numDisparities=numDisp,             # max_disp has to be dividable by 16 f. E. HH 192, 256
        blockSize=block,
        # wsize default 3; 5; 7 for SGBM reduced size image; 15 for SGBM full size image (1300px and above); 5 Works nicely
        P1=8 * 3 * 3 ** 2,
        P2=32 * 3 * 3 ** 2,
        disp12MaxDiff=1,
        uniquenessRatio=15,
        speckleWindowSize=0,
        speckleRange=2,
        preFilterCap=63,
        mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY
    )

    right_matcher = cv2.ximgproc.createRightMatcher(left_matcher)

    # FILTER Parameters
    lmbda = 80000
    sigma = 1.2
    visual_multiplier = 1.0

    wls_filter = cv2.ximgproc.createDisparityWLSFilter(matcher_left=left_matcher)
    wls_filter.setLambda(lmbda)
    wls_filter.setSigmaColor(sigma)

    print('computing disparity...')
    displ = left_matcher.compute(imgL, imgR)  # .astype(np.float32)/16
    dispr = right_matcher.compute(imgR, imgL)  # .astype(np.float32)/16
    displ = np.int16(displ)
    dispr = np.int16(dispr)
    filteredImg = wls_filter.filter(displ, imgL, None, dispr)  # important to put "imgL" here!!!

    filteredImg = cv2.normalize(src=filteredImg, dst=filteredImg, beta=0,
                                alpha=255, norm_type=cv2.NORM_MINMAX)
    filteredImg = np.uint8(filteredImg)
    # print(filteredImg)
    # plt.imshow(filteredImg)
    # plt.show()

    return filteredImg


# disparity(imgR, imgL, -10, 16, 3, 3)
