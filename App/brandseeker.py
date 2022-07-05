
from utils.general import (check_file, check_img_size, cv2, non_max_suppression)
from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages
from utils.torch_utils import select_device, time_sync

from utils.pdf_generator import pdf_generator, normalize
from utils.video_downloader import download
from utils.filtering import filter_output

from tqdm.autonotebook import tqdm
from pathlib import Path

import argparse
import torch

import cv2
import re


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


def predict(url, framerate, source, save_dir, save_unprocessed_output, alpha):

    if url:
        is_file = Path(url).suffix[1:] in (IMG_FORMATS + VID_FORMATS)
        is_url = url.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
        assert is_url, f"URL is incorrect ({url})"
        
        # Download the file or the youtube video
        if is_file:
            check_file(url, save_dir=source)
        else:
            # check if the url is a valid youtube url
            r = "((http(s)?:\/\/)?)(www\.)?((youtube\.com\/)|(youtu.be\/))[\S]+"
            assert re.match(r, url), f"The url needs to be a valid youtube url ({url})"

            # Download the video and save it to the specified path
            print('Downloading the video')
            if download(url, source):
                print('Successfully downloaded the video')
            else:
                print("Can't download the video")
        

    device = select_device('')
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='weights/best.pt')

    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size((640, 640), s=stride)  # check image size, might want to remove

    dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt, only_vids=True)
    assert dataset.nf == 1, f"There must be a single video file, {dataset.nf} were given"
    bs = 1  # batch_size

    brand_count = {}

    # Get some informations about the video
    path, im, im0s, vid_cap, s, frame = dataset.__iter__().__next__()
    initial_framerate = vid_cap.get(cv2.CAP_PROP_FPS)
    real_framerate = initial_framerate / round(initial_framerate / framerate)
    total_frames = dataset.frames
    dataset.frame = 0

    # Loop on frames
    pred_timing_start = time_sync()
    for path, im, im0s, vid_cap, s, frame in tqdm(dataset, total=total_frames):

        # skip the frame if it isn't in the specified framerate
        if frame % round(initial_framerate / framerate) != 0:
            continue

        im = torch.from_numpy(im).to(device)
        im = im.float()
        im /= 255  # 0 - 255 to 0.0 - 1.0

        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim

        # Inference
        pred = model(im)

        # NMS
        pred = non_max_suppression(pred, conf_thres=0.35, max_det=5)
        pred = pred[0].tolist()

        has_prediction = len(pred)
        if has_prediction:
            for brand in pred:
                label = names[int(brand[5])]

                # Retrieve or create a dictionnary key for the label and add the bbox, confidence and frame of the prediction
                brand_count[label] = brand_count.get(label, {"bbox": [], "confidence": [], "frame": []})
                brand_count[label]["bbox"].append(brand[0:4])
                brand_count[label]["confidence"].append(brand[4])
                brand_count[label]["frame"].append(frame)
    
    # Generate an output if a prediction has been made
    if save_unprocessed_output & bool(brand_count):
        with open(f"{save_dir}/{normalize(path)}.txt", "w") as f:
            f.write(str(brand_count))

    filtered_output = filter_output(brand_count, framerate, total_frames / initial_framerate, alpha=alpha)
    if filtered_output:
        pdf_generator(path, filtered_output, save_dir)
    else:
        print("No prediction has been made")


    pred_timing_stop = time_sync()
    pred_timing = pred_timing_stop - pred_timing_start
    print("Pred took %.2fs (%.2ffps)" % (pred_timing, ((total_frames / initial_framerate) * real_framerate) / pred_timing))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-U", "--url", help="A video url. It can be from youtube or a link to a file.")
    parser.add_argument("-F", "--framerate", type=int, default=15, help="The framerate of the analyzed video. A higher one will take longer to process.")
    parser.add_argument("-S", "--source", default="./input_video", help="The folder where your video is.")
    parser.add_argument("-O", "--save-dir", default="./predictions", help="The folder where the pdf with predictions will be.")
    parser.add_argument("-A", "--alpha", type=float, default=None, help="[0-1] A bigger alpha will give more importance to the confidence, otherwise the frames.")
    parser.add_argument("--save-unprocessed-output", default=False, action='store_true', help="Save an unprocessed dict containing all bounding boxes, frames and confidences.")
    args = parser.parse_args()
    predict(**vars(args))