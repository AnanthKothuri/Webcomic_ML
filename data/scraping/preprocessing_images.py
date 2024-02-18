from PIL import Image
from urllib.request import urlopen, Request
import os
import torch
import numpy as np
from torchvision import transforms
import sys
sys.path.insert(1, '../person_detection/')
from yolo_detection import detect_faces
from panel_segmentation_2 import segment_panel_2
from torchvision.transforms.functional import resize

SIZE = -1
NEW_SIZE = 512
transform_resize = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize(NEW_SIZE)
])
transform = transforms.ToTensor()
transform_to_image = transforms.ToPILImage()
total_saved = 0
link_count = 0


def save_image(section, link, count, dest, is_temp=False):
    global total_saved
    global NEW_SIZE
    if not is_temp:
        last_slash = link.rindex("/")
        path = "{}{}-{:03d}.jpg".format(dest, link[last_slash + 1: -5], count)
    else:
        path = f"{dest}/temp.jpg"

    # image = transform_to_image(section)
    # resized = transform_resize(image)
    # resized = center_crop_transform(resized)
    # section = transform(resized)
    # section = resize(section, (NEW_SIZE, NEW_SIZE))
    # print(section.shape)

    section *= 255
    section = section.permute(1, 2, 0)
    section = np.array(section, dtype=np.uint8)
    data = Image.fromarray(section)

    data.save(path)

def get_image_from_url(link):

    # printing info on number of images
    if link_count % 100 == 0:
        print("Link {}, total saved images: {}".format(link_count, total_saved))
    if 'png' not in link:
        raise ValueError('link is not to a png')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    req = Request(url=link, headers=headers)
    try:
        image_png = Image.open(urlopen(req))
    except:
        raise RuntimeError('could not load image from link')
    
    return image_png
    

def get_face_section(section, box):
    max_axis = max(box[2], box[3])
    max_height, max_width = section.shape[2], section.shape[1]
    left_x, right_x, top_y, bottom_y = box[0], box[0] + box[3], box[1], box[1] + box[2]
    if max_axis == box[2]:
        diff = int((box[2] - box[3]) / 2)
        left_x -= diff
        right_x += diff
        if left_x < 0:
            left_x = 0
            right_x = left_x + box[2]
        elif right_x > max_width:
            right_x = max_width
            left_x = right_x - box[2]

    elif max_axis == box[3]:
        diff = int((box[3] - box[2]) / 2)
        top_y -= diff
        bottom_y += diff
        if top_y < 0:
            top_y = 0
            bottom_y = top_y + box[3]
        elif bottom_y > max_height:
            bottom_y = max_height
            top_y = bottom_y - box[3]

    result = section[:, top_y:bottom_y, left_x:right_x]
    return result

def get_around_face_section(section, box):
    panel_height, panel_width = section.shape[1], section.shape[2]
    size = min(panel_height, panel_width)

    mid_y = box[1] + int(box[2] / 2)
    top_y = mid_y - int(size /2)
    bottom_y = mid_y + int(size/2)

    if top_y < 0:
        top_y = 0
        bottom_y = size
    if bottom_y >= panel_height:
        top_y = panel_height - size
        bottom_y = panel_height

    mid_x = box[0] + int(box[3] / 2)
    left_x = mid_x - int(size /2)
    right_x = mid_x + int(size/2)

    if left_x < 0:
        left_x = 0
        right_x = size
    if right_x >= panel_width:
        left_x = panel_width - size
        right_x = panel_width

    result = section[:, top_y:bottom_y, left_x:right_x]
    return result


def save_dataset2(input="image_links.txt", dest="/Users/ananthkothuri/Desktop/Solo_Leveling_Dataset/"):
    global total_saved
    global link_count
    global SIZE
    global NEW_SIZE
    
    if not os.path.exists(dest):
        os.mkdir(dest)
        os.mkdir(f'{dest}faces/')
        os.mkdir(f'{dest}people/')

    with open(input, "r") as file:
        image_links = file.readlines()

        for link in image_links:
            link_count += 1

            try:
                image_png = get_image_from_url(link)
                image_png_cpy = image_png.copy()
            except:
                continue
            large_image = transform(image_png_cpy)
            image = transform_resize(image_png)
            ratio = large_image.shape[2] // image.shape[2]
            SIZE = image.shape[2]

            # now we need to split images into SIZE x SIZE boxes with as little empty space
            count = 0
            panels = segment_panel_2(image.clone().permute(1, 2, 0))

            for panel in panels:
                panel = [x * ratio for x in panel]
                start_y, end_y = panel[0], panel[1]
                height = end_y - start_y
                width = panel[3] - panel[2]
                if height < width: continue

                section = large_image[:, start_y:end_y, :]
                path = f"{dest}/temp.jpg"

                try:
                    save_image(section.clone(), None, None, dest, is_temp=True)
                except:
                    print(f"couldn't save image of size {section.shape}")
                    continue

                has_faces, _, boxes, confidences = detect_faces(path) 
                if not has_faces:
                    os.remove(path)
                    continue

                for i in range(len(boxes)):
                    box = boxes[i]
                    conf = confidences[i]
                    if conf < 0.8: 
                        continue

                    # get only the face box
                    box_section = get_face_section(section.clone(), box)
                    try:
                        save_image(box_section.clone(), link, count, f'{dest}faces/')
                    except:
                        print(f"couldn't save image of size {section.shape}")
                        continue
                    count += 1
                    total_saved += 1


                    # get area around face
                    box_section = get_around_face_section(section.clone(), box)
                    try:
                        save_image(box_section.clone(), link, count, f'{dest}people/')
                    except:
                        print(f"couldn't save image of size {section.shape}")
                        continue
                    count += 1
                    total_saved += 1

                os.remove(path)