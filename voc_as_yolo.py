import os
import xml.etree.ElementTree as ET
import hashlib
from shutil import copyfile


def compute_sha1(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.sha1(f.read()).hexdigest()


def convert_coordinates(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_voc_to_yolo(voc_path, yolo_path):
    os.makedirs(yolo_path, exist_ok=True)
    os.makedirs(os.path.join(yolo_path, "image"), exist_ok=True)
    os.makedirs(os.path.join(yolo_path, "label"), exist_ok=True)
    # classes = []
    classes = [
        "jiangshi",
        "jiangshicunmin",
        "jiangshizhuling",
        "jiangshiyouzhushou",
        "jiangshima",
        "tuzi",
        "diaoling",
        "diaolingkulou",
        "jielueshou",
        "jieluezhe",
        "beijixiong",
        "weidaoshi",
        "faguangyouyu",
        "shilaimu",
        "mougu",
        "huanmozhe",
        "xiutanshou",
        "nvwu",
        "shouweizhe",
        "shiqiao",
        "shanyang",
        "yanjiangguai",
        "huanshushi",
        "huanyi",
        "ehun",
        "naogui",
        "yueling",
        "moyingren",
        "moyingman",
        "moyinglong",
        "cunmin",
        "hetun",
        "dongxuezhizhu",
        "liulangshangren",
        "liulangzhe",
        "haitun",
        "haigui",
        "nishi",
        "qianyingbei",
        "chizushou",
        "lieyanren",
        "redaiyu",
        "xiongmao",
        "niu",
        "qiuyu",
        "huli",
        "lang",
        "zhu",
        "zhuling",
        "zhulingmanbing",
        "mao",
        "youzhushou",
        "jianshouzhe",
        "yang",
        "yangtuo",
        "meixiyuan",
        "kulipa",
        "zhizhu",
        "mifeng",
        "kulou",
        "kedou",
        "bianfu",
        "duchong",
        "xingshangyangtuo",
        "baomao",
        "yuangushouweizhe",
        "tiekuilei",
        "xuekuilei",
        "qingwa",
        "ma",
        "lv",
        "luotuo",
        "luo",
        "kulouma",
        "youyu",
        "guiyu",
        "xueyu",
        "ji",
        "yingwu"
    ]
    for dirpath, dirnames, filenames in os.walk(voc_path):
        for filename in [f for f in filenames if f.endswith('.xml')]:
            xml_file = os.path.join(dirpath, filename)
            tree = ET.parse(xml_file)
            root = tree.getroot()
            size = root.find('size')
            w = int(size.find('width').text)
            h = int(size.find('height').text)

            for obj in root.iter('object'):
                cls = obj.find('name').text
                if cls not in classes:
                    classes.append(cls)
                    print('Found New Class:', cls)
                xmlbox = obj.find('bndbox')
                b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
                     float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
                bb = convert_coordinates((w, h), b)

                # SHA1 for image
                image_path = os.path.join(dirpath, root.find('filename').text)
                sha1 = compute_sha1(image_path)
                yolo_filename = "label/"+sha1 + '.txt'

                with open(os.path.join(yolo_path, yolo_filename), 'a') as yolo_file:
                    yolo_file.write(str(classes.index(cls)) +
                                    " " + " ".join([str(a) for a in bb]) + '\n')

                # Copy and rename image
                copyfile(image_path, os.path.join(
                    yolo_path, "image/"+sha1 + '.png'))

    # Save classes
    with open(os.path.join(yolo_path, 'classes.txt'), 'w') as class_file:
        for cls in classes:
            class_file.write(cls + '\n')


# Convert all VOC in 'voc_annotations' to YOLO format in 'yolo_annotations'
convert_voc_to_yolo('./', './yolo/')
