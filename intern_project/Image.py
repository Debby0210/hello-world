import numpy as np
import cv2

# 讀取圖片
image_path = 'car.jpg'  # 替換成你的圖片路徑
img = cv2.imread(image_path)

# 顯示圖片
cv2.imshow('Image', img)

# 等待按鍵事件，按任意鍵關閉視窗
cv2.waitKey(0)

# 關閉所有視窗
cv2.destroyAllWindows()
