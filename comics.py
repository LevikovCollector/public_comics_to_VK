import os
import requests
import pathlib
import datetime
import random
import shutil

LAST_COMICS_API = 'http://xkcd.com/info.0.json'

def create_folder(folder_name):
    os.makedirs(folder_name, exist_ok=True)

def create_file_path(dir, file_name):
    return pathlib.Path.joinpath(pathlib.Path.cwd(), dir, file_name)

def save_img(img_name, img_content, extension, folder_name = None, full_path = None):
    today = datetime.datetime.today().strftime("%d-%m-%Y_%H-%M")
    if folder_name:
        path = create_file_path(folder_name, f'{img_name}_{today}{extension}')
    else:
        path = pathlib.PurePath(full_path,f'{img_name}_{today}{extension}')

    with open(path, 'wb') as file:
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

    img_link = response.json()['img']
    img_extension = os.path.splitext(img_link.split('/')[-1])[1]

    img_response = requests.get(img_link)
    response.raise_for_status()

    return {
            'comics_content': img_response.content,
            'comics_comment': response.json()['alt'],
            'img_extension': img_extension
            }

def delete_comics(folder_with_img=None, full_path_to_folder=None):
    if folder_with_img:
        shutil.rmtree(pathlib.Path.joinpath(pathlib.Path.cwd(), folder_with_img))
    else:
        shutil.rmtree(full_path_to_folder)
