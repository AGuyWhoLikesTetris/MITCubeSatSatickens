import cv2
import numpy as np

# Read image
img = cv2.imread('color.jpg')

# threshold red
lower = np.array([0, 0, 0])
upper = np.array([40, 40, 255])
thresh = cv2.inRange(img, lower, upper)
    
# Change non-red to white
result = img.copy()
result[thresh != 255] = (255,255,255)

# save results
cv2.imwrite('color.jpg', thresh)
cv2.imwrite('color.jpg', result)

cv2.imshow('thresh', thresh)
cv2.imshow('result', result)
cv2.waitKey(0)
cv2.destroyAllWindows()