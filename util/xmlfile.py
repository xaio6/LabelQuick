import os
import xml.etree.ElementTree as ET


# 排版
def indent(elem, level=0):
    i = "\n" + level*"\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def xml(image_path, save_path, size, labels):
    root = ET.Element('annotation')
    folder_name = os.path.dirname(image_path)
    folder = ET.SubElement(root, 'folder')
    folder.text = folder_name

    file_name = os.path.basename(image_path)
    filename = ET.SubElement(root, 'filename')
    filename.text = file_name

    filepath = ET.SubElement(root, 'path')
    filepath.text = image_path

    img_size = ET.SubElement(root, 'size')
    width = ET.SubElement(img_size, 'width')
    width.text = str(size[0])
    height = ET.SubElement(img_size, 'height')
    height.text = str(size[1])
    depth = ET.SubElement(img_size, 'depth')
    depth.text = str(size[2])

    for dic in labels:
        object = ET.SubElement(root, 'object')

        lab_name = ET.SubElement(object, 'name')
        lab_name.text = dic['name']

        pose = ET.SubElement(object, 'pose')
        pose.text = dic['pose']

        truncated = ET.SubElement(object, 'truncated')
        truncated.text = str(dic['truncated'])

        difficult = ET.SubElement(object, 'difficult')
        difficult.text = str(dic['difficult'])

        bndbox = ET.SubElement(object, 'bndbox')
        xmin = ET.SubElement(bndbox, 'xmin')
        xmin.text = str(dic['bndbox'][0])
        ymin = ET.SubElement(bndbox, 'ymin')
        ymin.text = str(dic['bndbox'][1])
        xmax = ET.SubElement(bndbox, 'xmax')
        xmax.text = str(dic['bndbox'][2])
        ymax = ET.SubElement(bndbox, 'ymax')
        ymax.text = str(dic['bndbox'][3])

    indent(root)  # 格式化xml
    tree = ET.ElementTree(root)
    tree.write(save_path)  # 写入文件
    return tree


if __name__ == "__main__":
    path = r'dog.4019.jpg'
    save_path = "111.xml"
    size = [640, 640, 3]
    labels = [{'name': 'body',
               'pose': 'Unspecified',
               'truncated': 0,
               'difficult': 0,
               'bndbox': [9, 89, 297, 305]},
              {'name': 'body',
               'pose': 'Unspecified',
               'truncated': 0,
               'difficult': 1,
               'bndbox': [20, 89, 297, 350]}]

    print(xml(path,save_path, size, labels))
