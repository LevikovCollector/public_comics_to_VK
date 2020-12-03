import requests
import os
import pathlib
from dotenv import load_dotenv
API_VK = 'https://api.vk.com/method/'
API_VK_VER = '5.1269999'


def get_url_for_upload_img(path_to_folder):
    vk_params = {'access_token': os.getenv('ACCESS_TOKEN_VK'),
                 'v': API_VK_VER,
                 'group_id': os.getenv('GROUP_ID_VK')
                 }

    image = os.listdir(path_to_folder)[0]
    path_to_image = pathlib.PurePath(path_to_folder, image)

    with open(path_to_image, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.get(f'{API_VK}photos.getWallUploadServer', params=vk_params)
        verify_vk_respons(response.json())

        response = requests.post(response.json()['response']['upload_url'], files=files)
        verify_vk_respons(response.json())

        return response.json()

def post_img_to_vk_server(server_data):
    vk_params = {'access_token': os.getenv('ACCESS_TOKEN_VK'),
                 'v': API_VK_VER,
                 'group_id': os.getenv('GROUP_ID_VK'),
                 'server':server_data['server'],
                 'photo': server_data['photo'],
                 'hash': server_data['hash']
                 }

    response = requests.post(f'{API_VK}photos.saveWallPhoto', params=vk_params)
    verify_vk_respons(response.json())
    vk_response = response.json()['response'][0]
    return  {
             'media_id': vk_response['id'],
             'owner_id': vk_response['owner_id']
             }

def post_img_to_group_wall(attachments_info, message):
    vk_params = {'access_token': os.getenv('ACCESS_TOKEN_VK'),
                 'v': API_VK_VER,
                 'owner_id': f'-{os.getenv("GROUP_ID_VK")}',
                 'from_group': 1,
                 'attachments': f'photo{attachments_info["owner_id"]}_{attachments_info["media_id"]}',
                 'message': message
                }

    response = requests.post(f'{API_VK}wall.post', params=vk_params)
    verify_vk_respons(response.json())
    try:
        print(f'Комикс опубликован! ID записи: {response.json()["response"]["post_id"]}')
    except KeyError as e:
        print(f'При публикации возникли ошибки: {e.args}')

def verify_vk_respons(vk_response):
    try:
        error_key = vk_response['error']
        raise Exception(f'error_code: {error_key["error_code"]}, error_msg: {error_key["error_msg"]}')
    except KeyError:
        pass

