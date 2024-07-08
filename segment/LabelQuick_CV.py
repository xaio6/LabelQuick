import numpy as np
from segment_anything import sam_model_registry, SamPredictor
import cv2


class Anything_CV():
    def __init__(self, image):
        
        self.sam_checkpoint = r"C:\Users\zhaop\Desktop\segment-anything_GUI\segment\model\sam_vit_b_01ec64.pth"
        self.model_type = "vit_b"
        self.device = "cuda"
        
        #全局变量
        self.coords = []
        self.methods = []
        
        self.click_open = False
        self.option = False
        
        self.clicked_x = None
        self.clicked_y = None
        self.method = None
        
        #预测的结果
        self.masks = None
        self.scores = None
        self.logits = None
        
        self.mask = None
        
        self.x = None
        self.y = None
        self.w = None
        self.h = None
        
        #预加载模型
        self.sam = sam_model_registry[self.model_type](checkpoint=self.sam_checkpoint)
        self.sam.to(device=self.device)
        self.predictor = SamPredictor(self.sam)
        
        self.predictor.set_image(image)
        
        #初始图像
        self.image = image.copy()
        #画了点的图像
        self.image_dot = image.copy()  
        #画了mask的图像
        self.image_mask = image.copy()
        #用来保存mask的图像
        self.image_save = image.copy()
        
    #鼠标点击事件
    def Click_Event(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.clicked_x, self.clicked_y, self.method = x, y, 1
            self.click_open = True
        if event == cv2.EVENT_RBUTTONDOWN:
            self.clicked_x, self.clicked_y, self.method = x, y, 0
            self.click_open = True

    #键盘点击事件
    def Key_Event(self, key):
        if key == ord("s"):
            self.image_save = self.Draw_Mask(self.mask, self.image_save)
            
            self.image_dot = self.image.copy()
            self.image_mask = self.image_save.copy()
            
            self.coords = []
            self.methods = []
            
            print(self.x, self.y, self.w, self.h)
            
        elif key == ord("q"):
            self.image_dot = self.image.copy()
            self.image_mask = self.image_save.copy()
            
            self.coords = []
            self.methods = []
        #键盘的backspace键
        elif key == 8:

            self.image_dot = self.image.copy()
            self.image_mask = self.image.copy()
            self.image_save = self.image.copy()
                        
            self.coords = []
            self.methods = []
            
    #显示点
    def Draw_Point(self, image,label):
        if label == 1:
            cv2.circle(image, (self.clicked_x, self.clicked_y), 5, (255, 0, 0), -1) 
        elif label == 0:
            cv2.circle(image, (self.clicked_x, self.clicked_y), 5, (0, 0, 255), -1)
            
    #创建Mask
    def Create_Dot_Mask(self, win_name):
            cv2.setMouseCallback(win_name, self.Click_Event)
            if self.click_open:
                self.coords.append([self.clicked_x, self.clicked_y])
                self.methods.append(self.method)
                
                
                if self.option == False:
                    input_point = np.array(self.coords)
                    input_method = np.array(self.methods)

                    self.masks, self.scores, self.logits = self.predictor.predict(
                        point_coords = input_point,
                        point_labels = input_method,
                        multimask_output = True,
                    )
                    self.option = True

                else:
                    input_point = np.array(self.coords)
                    input_method = np.array(self.methods)
                    mask_input = self.logits[np.argmax(self.scores), :, :]  # Choose the model's best mask

                    self.masks, self.scores, self.logits  = self.predictor.predict(
                        point_coords = input_point,
                        point_labels = input_method,
                        mask_input = mask_input[None, :, :],
                        multimask_output = False,
                    )

                self.mask = self.masks[-1]
                self.click_open = False
                return self.mask
            else:
                return []     
    
    #画Mask
    def Draw_Mask(self, mask, image):
        # 获取轮廓
        h,w = mask.shape[-2:]
        mask = mask.reshape(h,w,1)
        white = np.zeros([h,w,1],dtype="uint8")
        white[:,:,0] = 255
        x = mask * white

        canny = cv2.Canny(x,50,100)
        # 画一个实心圆
        self.Draw_Point(image,self.method)
        img = image.copy()
        # 找到边缘轮廓
        contours, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 初始化最大面积和对应的最大轮廓
        max_area = 0
        max_contour = None

        # 遍历每个轮廓
        for contour in contours:
        # 计算轮廓的面积
            area = cv2.contourArea(contour)
            
            # 如果当前面积大于最大面积，则更新最大面积和对应的最大轮廓
            if area > max_area:
                max_area = area
                max_contour = contour
        # 使用矩形框绘制最大轮廓
        self.x, self.y, self.w, self.h = cv2.boundingRect(max_contour)
        cv2.rectangle(img, (self.x, self.y), (self.x + self.w, self.y + self.h), (0, 255, 0), 2)
        # 在原图上绘制边缘线
        cv2.drawContours(img, contours, -1, (0, 255, 0), 2)
        
        return img
    
    
if __name__ == '__main__':
    
    image = cv2.imread(r'C:\Users\zhaop\Desktop\segment-anything_GUI\image\fruits.jpg')
    ima = cv2.resize(image, (1000, 800))
    AD = Anything_CV(ima)
    
    while True:
        cv2.imshow('Image1', AD.image_mask)
        mask = AD.Create_Dot_Mask("Image1")
        keycode = cv2.waitKey(1)
        
        if keycode != -1:
            AD.Key_Event(keycode)
        
        if(mask != []):
            AD.image_mask = AD.Draw_Mask(mask, AD.image_dot)
    