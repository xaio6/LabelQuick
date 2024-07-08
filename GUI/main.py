import sys,os
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, QCoreApplication
import cv2
from util.QtFunc import *
from util.xmlfile import *
from GUI.UI_Main import Ui_MainWindow
from GUI.message import LabelInputDialog

sys.path.append("segment")
from segment.LabelQuick_QT import Anything_QT

class MainFunc(QMainWindow):
    def __init__(self):
        super(MainFunc, self).__init__()
        # 连接应用程序的 aboutToQuit 信号到自定义的槽函数
        QCoreApplication.instance().aboutToQuit.connect(self.clean_up)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 初始化属性
        self.current_index = 0
        self.image_files = None
        self.qImg = ""
        self.img_path = None
        self.image_path = None
        self.image = None
        self.image_name = None
        self.labels = []
        
        self.save_path = "./Temp"
        
        self.clicked_x = None
        self.clicked_y = None
        
        self.img_width = None 
        self.img_height = None
        
        self.AQ = Anything_QT()

        self.ui.actionOpen_Dir.triggered.connect(self.get_dir)
        self.ui.actionNext_Image.triggered.connect(self.next_img)
        self.ui.actionPrev_Image.triggered.connect(self.prev_img)
        self.ui.actionChange_Save_Dir.triggered.connect(self.set_save_path)

        #鼠标点击触发
        self.ui.label_3.mousePressEvent = self.mouse_press_event

    def get_dir(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory()
        if directory:
            self.image_files = list_images_in_directory(directory)
            self.current_index = 0
            self.show_path_image()
            
    def set_save_path(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory()
        if directory:
            self.save_path = directory
        
    def show_qt(self, img_path):
        #获取img_path名字
        self.image_name = os.path.basename(self.image_path).split('.')[0]
        
        Qt_Gui = QtGui.QPixmap(img_path)
        self.ui.label_2.setFixedSize(self.img_width, self.img_height)
        self.ui.label_2.setPixmap(Qt_Gui)

    def show_path_image(self):
        if self.image_files:
            self.image_path = self.image_files[self.current_index]
            self.img_path = self.image_path
            
            self.img_path, self.img_width, self.img_height = Change_image_Size(self.img_path)
            self.image = cv2.imread(self.img_path)
            self.AQ.Set_Image(self.image)
            self.show_qt(self.img_path)


    def next_img(self):
        if self.image_files and self.current_index < len(self.image_files) - 1:
            self.labels = []
            self.ui.listWidget.clear()
            self.current_index += 1
            self.show_path_image()
        else:
            upWindowsh("这是最后一张")

    def prev_img(self):
        if self.image_files and self.current_index > 0:
            self.labels = []
            self.ui.listWidget.clear()
            self.ui.listWidget.clearPropertyFlags()
            self.current_index -= 1
            self.show_path_image()
        else:
            upWindowsh("这是第一张")

    def mouse_press_event(self, event):
        x = event.x()
        y = event.y()
        
        if event.button() == Qt.LeftButton:
            self.clicked_x, self.clicked_y, self.method = x, y, 1
        if event.button() == Qt.RightButton:
            self.clicked_x, self.clicked_y, self.method = x, y, 0
        
        if(self.img_path != None):
            image = self.image.copy()
            self.AQ.Set_Clicked([x,y],self.method)
            self.AQ.Create_Mask()
            image = self.AQ.Draw_Mask(self.AQ.mask, image)
            
            cv2.imwrite("Temp/image.jpg", image)
            self.img_path = "Temp/image.jpg"
            self.show_qt(self.img_path)



    #重写QWidget类的keyPressEvent方法
    def keyPressEvent(self, event):
        if(self.img_path != None):
        # 打印按下的键的名称
            image = self.AQ.Key_Event(event.key())
            cv2.imwrite("Temp/image.jpg", image)
            self.img_path = "Temp/image.jpg"

            if(event.key() == 83):
                self.dialog = LabelInputDialog(self)
                self.dialog.show()
                self.dialog.confirmed.connect(self.on_dialog_confirmed)


            else:
                self.show_qt(self.img_path)
                super(QMainWindow, self).keyPressEvent(event)

    def on_dialog_confirmed(self, text):
        if text:
            self.ui.listWidget.addItem(text)
            file_path = os.path.join(self.save_path, f"{self.image_name}.xml")
            size = [self.img_width, self.img_height, 3]
            result = {
                'name': text,
                'pose': 'Unspecified',
                'truncated': 0,
                'difficult': 0,
                'bndbox': [self.AQ.x, self.AQ.y, self.AQ.w, self.AQ.h]
            }
            self.labels.append(result)
            xml(self.image_path, file_path, size, self.labels)

    def clean_up(self):
        file_path = 'GUI/history.txt'
        if os.path.exists(file_path):
            os.remove(file_path)










        
