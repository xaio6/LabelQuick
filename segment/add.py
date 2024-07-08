import numpy as np
import torch
from segment_anything import sam_model_registry, SamPredictor
import matplotlib.pyplot as plt
import cv2
import sys

def click_event(event, x, y, flags, param):
    global clicked_x, clicked_y
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_x, clicked_y = x, y

image = cv2.imread('notebooks/images/groceries.jpg')
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image = cv2.resize(image, (1000, 800))


sam_checkpoint = "model/sam_vit_b_01ec64.pth"
model_type = "vit_b"
device = "cuda"
sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)
predictor = SamPredictor(sam)
predictor.set_image(image)

cv2.imshow('Image1', image)
cv2.setMouseCallback('Image1', click_event)

while True:
    print("111")
    cv2.imshow('Image1', image)
    cv2.setMouseCallback('Image1', click_event)
    print("222")
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if 'clicked_x' in globals() and 'clicked_y' in globals():
        x = clicked_x
        y = clicked_y
        print(f"Clicked at ({x}, {y})")

        input_point = np.array([[x, y]])
        input_label = np.array([1])

        masks, scores, logits = predictor.predict(
            point_coords=input_point,
            point_labels=input_label,
            multimask_output=True,
            )
        print(scores)

        mask = masks[-1]


        h,w = mask.shape[-2:]
        mask = mask.reshape(h,w,1)
        white = np.zeros([h,w,1],dtype="uint8")
        white[:,:,0] = 255
        x = mask * white

        canny = cv2.Canny(x,50,100)
 
        # im = image.copy()
        # im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)

        # 找到边缘轮廓
        contours, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # 在原图上绘制边缘线
        cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

        # 显示带有边缘的照片
        cv2.imshow('Image1', image)

        # 重置点击坐标
        del clicked_x, clicked_y

cv2.destroyAllWindows()
