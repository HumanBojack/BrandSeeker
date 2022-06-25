import argparse
# from models.yolov5 import utils
# utils.notebook_init()
# from models.yolov5 import detect
import torch
from PIL import Image
import cv2

# from models.yolov5.models.common import DetectMultiBackend

from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadStreams
from utils.general import (LOGGER, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2, increment_path, non_max_suppression, print_args, scale_coords, strip_optimizer, xyxy2xywh)
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device, time_sync

from pathlib import Path

# weights=ROOT / 'yolov5s.pt',  # model.pt path(s)
# source=ROOT / 'data/images',  # file/dir/URL/glob, 0 for webcam
# data=ROOT / 'data/coco128.yaml',  # dataset.yaml path
# imgsz=(640, 640),  # inference size (height, width)
# conf_thres=0.25,  # confidence threshold
# iou_thres=0.45,  # NMS IOU threshold
# max_det=1000,  # maximum detections per image
# device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
# view_img=False,  # show results
# save_txt=False,  # save results to *.txt
# save_conf=False,  # save confidences in --save-txt labels
# save_crop=False,  # save cropped prediction boxes
# nosave=False,  # do not save images/videos
# classes=None,  # filter by class: --class 0, or --class 0 2 3
# agnostic_nms=False,  # class-agnostic NMS
# augment=False,  # augmented inference
# visualize=False,  # visualize features
# update=False,  # update all models
# project=ROOT / 'runs/detect',  # save results to project/name
# name='exp',  # save results to project/name
# exist_ok=False,  # existing project/name ok, do not increment
# line_thickness=3,  # bounding box thickness (pixels)
# hide_labels=False,  # hide labels
# hide_conf=False,  # hide confidences
# half=False,  # use FP16 half-precision inference
# dnn=False,  # use OpenCV DNN for ONNX inference


def predict(args):
    print(args)

    if args['model'] == 'yolo':

        source = "./images" # needs to be changed later

        is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS)
        is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
        if is_url and is_file:
            source = check_file(source)

        save_dir = "./predictions"

        device = select_device('')
        model = torch.hub.load('ultralytics/yolov5', 'custom', path='weights/best.pt')

        stride, names, pt = model.stride, model.names, model.pt
        imgsz = check_img_size((640, 640), s=stride)  # check image size might want to remove

        dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt)
        bs = 1  # batch_size

        dt, seen = [0.0, 0.0, 0.0], 0
        for path, im, im0s, vid_cap, s in dataset:
            t1 = time_sync()
            im = torch.from_numpy(im).to(device)
            im = im.float()
            im /= 255  # 0 - 255 to 0.0 - 1.0

            if len(im.shape) == 3:
                im = im[None]  # expand for batch dim
            t2 = time_sync()
            dt[0] += t2 - t1

            # Inference
            pred = model(im)
            t3 = time_sync()
            dt[1] += t3 - t2

            # NMS
            pred = non_max_suppression(pred, conf_thres=0.35, max_det=5) # might want to discuss the max nb of detection, iou...
            dt[2] += time_sync() - t3

            frame = getattr(dataset, 'frame', 0)

            print(pred)
            
            # for i, det in enumerate(pred):  # per image
            #     seen += 1
            #     p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)

            #     p = Path(p)  # to Path
            #     # save_path = str(save_dir / p.name)  # im.jpg
            #     # txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # im.txt

            #     s += '%gx%g ' % im.shape[2:]  # print string
            #     gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            #     # imc = im0.copy() if save_crop else im0  # for save_crop
            #     # imc = im0
            #     # annotator = Annotator(im0, line_width=line_thickness, example=str(names))





        # results = model(imgs, size=640)
        # results.print()
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-M", "--model", choices=["yolo"], default="yolo", help="choose the used model")
    group.add_argument("-U", "--url", help="A youtube url of a video. The model will be yolo and the images and videos folder will be ignored")
    parser.add_argument("-F", "--framerate", type=int, default=15, help="the framerate of the video, only works on videos")
    # Add a data source argument
    # remove the model choice?
    args = parser.parse_args()

    predict(vars(args))