import os
import xml.etree.ElementTree as ET
import hashlib
from shutil import copyfile

def count_statistics(voc_path):
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
    image_count = 0
    box_count = 0
    class_stats = {cls: {'box_count': 0, 'image_count': 0} for cls in classes}

    for dirpath, dirnames, filenames in os.walk(voc_path):
        for filename in [f for f in filenames if f.endswith('.xml')]:
            xml_file = os.path.join(dirpath, filename)
            tree = ET.parse(xml_file)
            root = tree.getroot()
            image_count += 1
            clsl=set()
            for obj in root.iter('object'):
                cls = obj.find('name').text
                if cls not in classes:
                    classes.append(cls)
                    class_stats[cls] = {'box_count': 0, 'image_count': 0}
                    print('Found New Class:', cls)
                clsl.add(cls)
                class_stats[cls]['box_count'] += 1
                box_count += 1
            for cls in clsl:
                class_stats[cls]['image_count'] += 1

    print(f"Total Images: {image_count}")
    print(f"Total Boxes: {box_count}")
    print("-------------------------------------------------")
    print("image_count Sort")
    sorted_class_stats = sorted(class_stats.items(), key=lambda item: item[1]['image_count'], reverse=True)
    for cls, stats in sorted_class_stats:
        print(f"Class: {cls}, Boxes: {stats['box_count']}, Images: {stats['image_count']}")
    print("-------------------------------------------------")
    print("box_count Sort")
    sorted_class_stats = sorted(class_stats.items(), key=lambda item: item[1]['box_count'], reverse=True)
    for cls, stats in sorted_class_stats:
        print(f"Class: {cls}, Boxes: {stats['box_count']}, Images: {stats['image_count']}")
    
    # for cls, stats in class_stats.items():
    #     print(f"Class: {cls}, Boxes: {stats['box_count']}, Images: {stats['image_count']}")

# Count statistics for all VOC in 'voc_annotations'
count_statistics('./')
