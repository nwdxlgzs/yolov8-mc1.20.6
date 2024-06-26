from ultralytics import YOLO

def main():
    modelName = 'yolov8n.pt'
    device=[0]
    model = YOLO(modelName)
    # 预训练阶段每种生物数量相对均衡，而且数量相对较少，这个阶段模型学习基本的特征细节并巩固为思想钢印
    model.train(data="data-pretrain.yaml", model=modelName, device=device, batch=1, epochs=100, imgsz=1920)
    modelName = 'pretrain.pt'
    model.save(modelName)
    # 微调阶段，所有数据一并训练，各个生物数量差距较大，依赖预训练阶段的思想钢印抵消一部分缺陷，然后学习更多样本和实际场景
    model.train(data="data.yaml", model=modelName, device=device, batch=1, epochs=100, imgsz=1920)
if __name__ == '__main__':
    main()
