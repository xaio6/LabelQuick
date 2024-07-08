# LabelQuick
一种快速、轻松的AI辅助标注工具LabelQuick

![labelquick](https://github.com/xaio6/LabelQuick/assets/118904918/144686bc-7b64-4cf6-bad9-fc389fd0817d)


### 项目更新
🔥 V1.0 : 2024/7/8: 我们更新了模型仓库的运行文件和配置文件，开源基础的UI跟标注功能，主要用于Yolov5的数据标注。

### 简介
LabelQuick 是一款由 AI Horizon 团队设计并开发的快速图像标注工具，目前处于初步开发阶段。它提供了直观易用的界面和强大的标注与分割功能，帮助您高效完成数据集的标注工作。当前版本仅支持 Windows 系统。

![1](https://github.com/xaio6/LabelQuick/assets/118904918/bd06d644-7dbf-4240-89e7-1b55c7a7679a)


### 快速开始
1. 安装 `requirements` 中的依赖。
2. 下载[模型](https://pan.baidu.com/s/16xAgfkCgpDHR9eo2xoUIaQ?pwd=AIHZ)到 `segment/model` 里面。
3. 运行 `Run.py` 打开 LabelQuick，点击 "OpenDir" 打开您的图片数据集。
4. 点击 `Open Dir` 选择图片目录。
5. 点击 `Change Save Dir` 选择标注数据保存目录。
6. 使用鼠标左键单击图片开始标注您的数据。
7. 完成标注后，并导出标注数据。

### 用户界面介绍
- **顶部菜单栏**：包含文件、编辑、视图等常用功能。
- **左侧工具栏**：打开文件夹、选择标注数据储存位置。
- **中央工作区**：展示您的数据集，供您进行标注。
- **右侧属性面板**：显示当前数据集的标签。



### 功能详解
- **快速标注**：1.0 版本快速打标，只需鼠标左键单击标注对象，软件将自动识别物品最大边缘的最小矩形框并进行快速自动标注。
- **数据管理**：轻松导入、导出和管理您的数据集。

### 产品亮点
- 相比传统手动打标，LabelQuick 可以更快速地进行数据标注工作。
![2](https://github.com/xaio6/LabelQuick/assets/118904918/07221533-0d99-485f-84c9-0e1dca4855b7)
- 与 labelimg 和 Labelme 不同，LabelQuick 只需鼠标单击即可完成标注，大大提高了标注效率；标注准确度达到 0.9，比传统手动打标更精准。
![3](https://github.com/xaio6/LabelQuick/assets/118904918/9e5b137d-8482-4315-965e-3c483f2fb38f)

### Demo


https://github.com/xaio6/LabelQuick/assets/118904918/201647df-3544-4030-84c4-b719f8a909bf



### 常见问题解答（FAQ）
- **Q:** 如何撤销错误的标注？  
  **A:** 使用快捷键 (Q 或 Delete 键)。
- **Q:** 有哪些快捷键？  
  **A:** 上一张：A；下一张：D；保存标注数据：S。

### 友情链接
- [SegmentAnything](https://github.com/facebookresearch/segment-anything):分割任何模型 （SAM）

### 技术支持和联系方式
如果您在使用过程中遇到任何问题，请联系我们的技术支持团队：
- 公众号：AI Horizon

![5d2d299e21c40ef9bbe17b5b1e09fda](https://github.com/xaio6/LabelQuick/assets/118904918/17e51083-3abc-4812-9d32-8819f85cb3be)




感谢您选择 LabelQuick，我们希望这款工具能极大地提升您的工作效率。祝您标注愉快！
