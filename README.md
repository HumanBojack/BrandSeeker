# BrandSeeker
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1ACWrzkK7HLayllfno8cQ8iF9-1gYkx5g?usp=sharing)
[![Open in Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/code/humanbojack/brandseeker)

This repository uses methods from [the yolov5 🚀 repository](https://github.com/ultralytics/yolov5). Our dataset can be found [here](https://www.kaggle.com/datasets/humanbojack/yolo-brand-object-detection).

# What is BrandSeeker?
This project aims at creating a CLI tool that detects brands in a video.
<details>
<summary>The brands that can be recognized (click to expand)</summary>
["Republic of Gamers", "Hello Fresh", "Displate", "KiwiCo", "World of Tanks", "Dollar Shave Club", "SkillShare", "Manscaped", "Rhinoshield", "Raid shadow legends", "Worlds of Warships", "Fruitz", "War Thunder", "Redbull", "Squarespace", "Brilliant.org", "Logitech", "DBrand", "Honey coupon", "Gorillas brand", "levlup", "Ridge wallet", "ExpressVPN", "State of Survival", "Coca Cola", "Crunchyroll", "Uber Eats", "Surfshark", "Corsair", "Lootcrate", "Amazon", "audible", "NordVPN", "GFuel", "Genshin Impact", "TunnelBear VPN", "Microsoft", "Winamax"]
</details>

# The tool
## Installation
You will need **python>=3.7** and **pytorch**.
```bash
git clone https://github.com/HumanBojack/BrandSeeker
cd BrandSeeker/App
pip install -r requirements.txt
```

## Usage
> **Note**: In order to make easier and faster predictions, we recommand using [Colab or Kaggle](#brandseeker).

First, place your video in the **input_video** folder.

Then, in your terminal, run:
```bash
# BrandSeeker/App
python brandseeker.py
```

You might also want to change some parameters.
```
$ python brandseeker.py --help

usage: brandseeker.py [-h] [-U URL] [-F FRAMERATE] [-S SOURCE] [-O SAVE_DIR] [-A ALPHA] [--save-unprocessed-output]

options:
  -h, --help            show this help message and exit
  -U URL, --url URL     A video url. It can be from youtube or a link to a file. (default: None)
  -F FRAMERATE, --framerate FRAMERATE
                        The framerate of the analyzed video. A higher one will take longer to process. (default: 15)
  -S SOURCE, --source SOURCE
                        The folder where your video is. (default: ./input_video)
  -O SAVE_DIR, --save-dir SAVE_DIR
                        The folder where the pdf with predictions will be. (default: ./predictions)
  -A ALPHA, --alpha ALPHA
                        [0-1] A bigger alpha will give more importance to the confidence, otherwise the frames. (default: None)
  --save-unprocessed-output
                        Save an unprocessed dict containing all bounding boxes, frames and confidences. (default: False)
```

Finally, you can get the outputs in the **predictions** folder.
