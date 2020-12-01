import requests
import os
import pathlib

API_VK = 'https://api.vk.com/method/'
API_VK_VER = '5.126'


def get_url_for_upload_img():
    vk_params = {'access_token': os.getenv('ACCESS_TOKEN'),
                 'v': API_VK_VER,
                 'group_id': os.getenv('GROUP_ID')
                 }

    image = os.listdir(pathlib.Path.joinpath(pathlib.Path.cwd(), 'images'))[0]
    path_to_image = pathlib.Path.joinpath(pathlib.Path.cwd(), 'images', image)

    with open(path_to_image, 'rb') as file:
        files = {
            'photo': file,
        }
        respons = requests.get(f'{API_VK}photos.getWallUploadServer', params=vk_params)
        respons.raise_for_status()

        respons = requests.post(respons.json()['response']['upload_url'], files=files)
        respons.raise_for_status()

        return respons.json()

def post_img_to_vk_server(server_data):
    vk_params = {'access_token': os.getenv('ACCESS_TOKEN'),
                 'v': API_VK_VER,
                 'group_id': os.getenv('GROUP_ID'),
                 'server':server_data['server'],
                 'photo': server_data['photo'],
                 'hash': server_data['hash']
                 }

    respons = requests.post(f'{API_VK}photos.saveWallPhoto', params=vk_params)
    respons.raise_for_status()

    return  {
             'media_id': respons.json()['response'][0]['id'],
             'owner_id': respons.json()['response'][0]['owner_id']
             }

def post_img_to_group_wall(attachments_info, message):
    vk_params = {'access_token': os.getenv('ACCESS_TOKEN'),
                 'v': API_VK_VER,
                 'owner_id': f'-{os.getenv("GROUP_ID")}',
                 'from_group': 1,
                 'attachments': f'photo{attachments_info["owner_id"]}_{attachments_info["media_id"]}',
                 'message': message
                }

    respons = requests.post(f'{API_VK}wall.post', params=vk_params)
    respons.raise_for_status()
    try:
        print(f'Комикс опубликован! ID записи: {respons.json()["response"]["post_id"]}')
    except KeyError as e:
        print(f'При публикации возникли ошибки: {e.args}')
