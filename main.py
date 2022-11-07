from pathlib import Path
import cv2
import matplotlib.pyplot as plt
from rembg import remove
import numpy as np
import click
import mimetypes

ASPECT = 4/5
BUFFER = 0.1

def calc_coord_from_contours(contours, height):
    # 輪郭の座標をリストに代入していく
    x1 = [] #x座標の最小値
    y1 = [] #y座標の最小値
    x2 = [] #x座標の最大値
    y2 = [] #y座標の最大値
    for i in range(1, len(contours)):# i = 1 は画像全体の外枠になるのでカウントに入れない
        ret = cv2.boundingRect(contours[i])
        x1.append(ret[0])
        y1.append(ret[1])
        x2.append(ret[0] + ret[2])
        y2.append(ret[1] + ret[3])

    # 輪郭の一番外枠を切り抜き
    x1_min = min(x1)
    y1_min = min(y1) + int(height * 0.03)
    x2_max = max(x2)
    y2_max = max(y2)
    return x1_min, y1_min, x2_max, y2_max

def adjust_frame_from_image_size (
        min_length, 
        max_length, 
        diff,
        target_length
):
    max_length = int(max_length + diff)
    min_length = int(min_length - diff)
    if min_length < 0 or max_length > target_length:
        if abs(min_length) > max_length - target_length:
            min_length = 0
            max_length = max_length + min_length
        else:
            min_length = min_length + (max_length-target_length)
            max_length = target_length
    return min_length, max_length

def trim_whole_image(input_image: np.array) -> np.array: 
    output = remove(input_image) 

    #2値化
    img2gray = cv2.cvtColor(output,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 0, 255, cv2.THRESH_BINARY)

    height, width, channel = input_image.shape
    # 輪郭を抽出
    contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    x1_min, y1_min, x2_max, y2_max = calc_coord_from_contours(contours, height)

    frame_width = x2_max - x1_min
    frame_height = y2_max - y1_min

    if frame_height * ASPECT > frame_width:
        diff = (frame_height * ASPECT - frame_width) /2 
        x1_min, x2_max = adjust_frame_from_image_size(
            x1_min, x2_max, diff, width
        )
    else:
        diff = (frame_width / ASPECT - frame_height) /2 
        y1_min, y2_max = adjust_frame_from_image_size(
            y1_min, y2_max, diff, height
        )

    crop_img = input_image[y1_min:y2_max, x1_min:x2_max]
    return crop_img

def trim_detail_image(input_image: np.array) -> np.array:
    height, width, channel = input_image.shape

    if height * ASPECT > width:
        diff = (height - width/ASPECT) /2 
        y_min = int(diff)
        y_max = int(height - diff)
        x_min = 0
        x_max = width
    else:
        diff = (width - height * ASPECT) /2 
        y_max = height
        y_min = 0
        x_min = int(diff)
        x_max = int(width - diff)

    crop_img = input_image[y_min:y_max, x_min:x_max] 
    return crop_img 

@click.command()
@click.argument('path')
def main(path):
    images_dir = "input" / Path(path)
    output_dir = "output" / Path(path)
    output_dir.mkdir(exist_ok=True)
    images = list(images_dir.iterdir())
    for image in images:
        if mimetypes.guess_type(image)[0] != "image/jpeg":
            continue
        input_image = cv2.imread(str(image)) 
        if image.stem.startswith("whole"):
            print(f"whole start: {image.name}")
            crop_img = trim_whole_image(input_image)
        else:
            print(f"detail start: {image.name}")
            crop_img = trim_detail_image(input_image)
        cv2.imwrite(str(output_dir / image.name), crop_img)

if __name__ == "__main__":
    main()


