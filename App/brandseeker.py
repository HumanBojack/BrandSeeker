import argparse
# from models.yolov5 import utils
# utils.notebook_init()
# from models.yolov5 import detect
import torch
from PIL import Image
import cv2
from fpdf import FPDF

def predict(args):
    print(args)

    if args['model'] == 'yolo':
        # model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
        model = torch.hub.load('ultralytics/yolov5', 'custom', path='models/yolov5/best.pt')
        # model = torch.hub.load('App/models/yolov5/', 'custom', path='App/models/yolov5/best.pt', source='local')

        # img = Image.open("App/images/AWD_Thumbnail_2.png")
        imgs = []
        imgs.append(cv2.imread("images/uber-eats-jupdlc.jpg"))

        results = model(imgs, size=640)

        results.print()
    
    # Pdf example
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, 'Hello World!')
    pdf.output('predictions/result.pdf', 'F')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-M", "--model", choices=["yolo"], default="yolo", help="choose the used model")
    group.add_argument("-P", "--pdf", help="Export result to pdf")
    group.add_argument("-U", "--url", help="A youtube url of a video. The model will be yolo and the images and videos folder will be ignored")
    parser.add_argument("-F", "--framerate", type=int, default=15, help="the framerate of the video, only works on videos")
    args = parser.parse_args()

    predict(vars(args))