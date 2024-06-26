import os

# 扫描指定目录
def scan_directory(directory):
    png_files = set()
    xml_files = set()

    # 遍历目录中的所有文件和子目录
    for filename in os.listdir(directory):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            png_files.add(filename[:-4])
        elif filename.endswith('.xml'):
            xml_files.add(filename[:-4])

    # 查找不匹配的文件
    unmatched_png = png_files - xml_files
    unmatched_xml = xml_files - png_files

    # 打印结果
    if unmatched_png or unmatched_xml:
        print(f"In directory '{directory}':")
        for file in unmatched_png:
            print(f"Missing XML: {file}.png")
        for file in unmatched_xml:
            print(f"Missing PNG: {file}.xml")

# 遍历当前目录及其所有子目录
for root, dirs, files in os.walk("."):
    scan_directory(root)
