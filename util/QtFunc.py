import os
from PIL import Image


from PyQt5.QtWidgets import QMainWindow,QApplication,QMessageBox

def upWindowsh(hint):
    messBox = QMessageBox()
    messBox.setWindowTitle(u'提示')
    messBox.setText(hint)
    messBox.exec_()
    
    

def list_images_in_directory(directory):
    image_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                image_files.append(os.path.join(root, file))
    return image_files

# 修改照片大小
def Change_image_Size(image_path):
    # 打开原图像
    original_image = Image.open(image_path)
    # 获取照片大小
    width, height = original_image.size
    if width > 1051:
        ratio = 1051 / width
        width = 1051
        height *= ratio
        reduced_image = original_image.resize((int(width),int(height)))
        reduced_image.save((image_path))
    if height > 721:
        ratio = 721 / height
        height = 721
        width *= ratio
        reduced_image = original_image.resize((int(width),int(height)))
        reduced_image.save((image_path))
    return image_path, width, height