import os
import requests
import pathlib
import datetime
import random

LAST_COMICS_API = 'http://xkcd.com/info.0.json'

def create_folder(folder_name):
    os.makedirs(folder_name, exist_ok=True)

def create_file_path(dir, file_name):
    return pathlib.Path.joinpath(pathlib.Path.cwd(), dir, file_name)

def save_img(img_name, img_content, extension):
    today = datetime.datetime.today().strftime("%d-%m-%Y_%H-%M")
    with open(create_file_path('images', f'{img_name}_{today}.{extension}'), 'wb') as file:
        file.write(img_content)

def get_num_comics():
    response = requests.get(LAST_COMICS_API)
    response.raise_for_status()

    return  response.json()['num']

def get_comics():
    all_comics_num = get_num_comics()
    comics_num = random.randint(0, all_comics_num)

    response = requests.get(f'http://xkcd.com/{comics_num}/info.0.json')
    response.raise_for_status()

    img_response = requests.get(response.json()['img'])
    response.raise_for_status()

    return {
            'comics_content': img_response.content,
            'comics_comment': response.json()['alt']
            }

def delete_comics():
    image = os.listdir(pathlib.Path.joinpath(pathlib.Path.cwd(), 'images'))[0]
    path_to_image = pathlib.Path.joinpath(pathlib.Path.cwd(), 'images', image)
    os.remove(path_to_image)