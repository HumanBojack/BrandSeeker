import argparse
# from models.yolov5 import utils
# utils.notebook_init()
# from models.yolov5 import detect
import torch
from PIL import Image
import cv2


def predict(args):
    print(args)

    if args['model'] == 'yolo':
        # model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
        model = torch.hub.load('ultralytics/yolov5', 'custom', path='App/models/yolov5/best.pt')
        # model = torch.hub.load('App/models/yolov5/', 'custom', path='App/models/yolov5/best.pt', source='local')

        # img = Image.open("App/images/AWD_Thumbnail_2.png")
        imgs = []
        imgs.append(cv2.imread("App/images/AWD_Thumbnail_2.png"))
        # img = Image.open("App/images/uber-eats-1024x682.jpg")
        imgs.append(cv2.imread("App/images/uber-eats-1024x682.jpg"))
        # img = Image.open("App/images/asus_g513qc_bb74_g15_ryzen_7_5800h_1633645.jpg")
        imgs.append(cv2.imread("App/images/asus_g513qc_bb74_g15_ryzen_7_5800h_1633645.jpg"))
        # detect.run() # weights="App/models/yolov5/best.pt"

        results = model(imgs, size=640)

        results.print()
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-M", "--model", choices=["yolo"], default="yolo", help="choose the used model")
    group.add_argument("-U", "--url", help="A youtube url of a video. The model will be yolo and the images and videos folder will be ignored")
    parser.add_argument("-F", "--framerate", type=int, default=15, help="the framerate of the video, only works on videos")
    args = parser.parse_args()

    predict(vars(args))