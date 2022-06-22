import argparse
# from models.yolov5 import utils
# utils.notebook_init()
# from models.yolov5.detect import run
import torch


def predict(args):
    print(args)

    if args['model'] == 'yolo':
        print('hello')
        # detect.run() # weights="App/models/yolov5/best.pt"
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-M", "--model", choices=["yolo"], default="yolo", help="choose the used model")
    group.add_argument("-U", "--url", help="A youtube url of a video. The model will be yolo and the images and videos folder will be ignored")
    parser.add_argument("-F", "--framerate", type=int, default=15, help="the framerate of the video, only works on videos")
    args = parser.parse_args()

    predict(vars(args))

