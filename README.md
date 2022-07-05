# BrandSeeker
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1ACWrzkK7HLayllfno8cQ8iF9-1gYkx5g?usp=sharing)
<!-- [![Open in Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)]() -->

This repository uses methods from [the yolov5 🚀 repository](https://github.com/ultralytics/yolov5).

# What is BrandSeeker?
This project aims at creating a CLI tool that detects brands in a video. We want to 
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

usage: brandseeker.py [-h] [-U URL] [-F FRAMERATE] [-S SOURCE] [-O SAVE_DIR]

options:
  -h, --help            show this help message and exit
  -U URL, --url URL     A youtube url of a video. The model will be yolo and the images and videos folder will be ignored (default: None)
  -F FRAMERATE, --framerate FRAMERATE
                        The framerate of the analyzed video. A higher one will take longer to process. (default: 15)
  -S SOURCE, --source SOURCE
                        The folder where your video is. (default: ./input_video)
  -O SAVE_DIR, --save-dir SAVE_DIR
                        The folder where the pdf with predictions will be. (default: ./predictions)
```

Finally, you can get the outputs in the **predictions** folder.
