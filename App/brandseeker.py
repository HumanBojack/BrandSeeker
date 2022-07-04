import argparse
# from models.yolov5 import utils
# utils.notebook_init()
# from models.yolov5 import detect
import torch
from PIL import Image
import cv2

from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadStreams
from utils.general import (LOGGER, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2, increment_path, non_max_suppression, print_args, scale_coords, strip_optimizer, xyxy2xywh)
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device, time_sync

from pathlib import Path

from tqdm import tqdm

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


def predict(url, framerate, source, save_dir):

    is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS)
    is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
    if is_url and is_file:
        source = check_file(source)

    device = select_device('')
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='weights/best.pt')

    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size((640, 640), s=stride)  # check image size might want to remove

    dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt, only_vids=True)
    assert dataset.nf == 1, f"There must be a single video file, {dataset.nf} were given"
    bs = 1  # batch_size

    # Get some informations about the video
    path, im, im0s, vid_cap, s, frame = dataset.__iter__().__next__()
    initial_framerate = vid_cap.get(cv2.CAP_PROP_FPS)
    real_framerate = initial_framerate / round(initial_framerate / framerate)
    total_frames = dataset.frames
    dataset.frame = 0


    pred_timing_start = time_sync()
    dt, seen = [0.0, 0.0, 0.0], 0
    for path, im, im0s, vid_cap, s, frame in tqdm(dataset, total=total_frames):

        # skip the frame if it isn't in the specified framerate
        if frame % round(initial_framerate / framerate) != 0:
            continue

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
        pred = non_max_suppression(pred, conf_thres=0.35, max_det=5)
        dt[2] += time_sync() - t3


        has_prediction = len(pred[0])
        # if has_prediction:
        #     print(s) # save to the file

    pred_timing_stop = time_sync()
    pred_timing = pred_timing_stop - pred_timing_start
    print(f"Pred took {pred_timing}s ({pred_timing / real_framerate}fps)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-U", "--url", help="A youtube url of a video. The model will be yolo and the images and videos folder will be ignored")
    parser.add_argument("-F", "--framerate", type=int, default=15, help="The framerate of the analyzed video. A higher one will take longer to process.")
    parser.add_argument("-S", "--source", default="./input_video", help="The folder where your video is.")
    parser.add_argument("-O", "--save-dir", default="./predictions", help="The folder where the pdf with predictions will be.")
    args = parser.parse_args()

    predict(**vars(args))