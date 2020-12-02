from api_VK import get_url_for_upload_img, post_img_to_vk_server, post_img_to_group_wall
from comics import get_comics, create_folder, save_img, delete_comics
from dotenv import load_dotenv
import argparse
import pathlib

if __name__== '__main__':
    load_dotenv(dotenv_path='.env')
    parser = argparse.ArgumentParser(description='Введите название папки для изображений')
    parser.add_argument('--full_path_to_image', help='Полный путь к папке с комиксами', default=None)
    parser.add_argument('--image_folder_name', help='Путь к папке с комиксами', default='images')
    args = parser.parse_args()

    try:
        new_comics = get_comics()
        if args.full_path_to_image:
            create_folder(args.full_path_to_image)
            save_img('img', new_comics['comics_content'], new_comics['img_extension'],
                     full_path=args.full_path_to_image)
            server_data = get_url_for_upload_img(args.full_path_to_image)
        else:
            create_folder(args.image_folder_name)
            save_img('img', new_comics['comics_content'], new_comics['img_extension'],
                     folder_name=args.image_folder_name)
            server_data = get_url_for_upload_img(pathlib.Path.joinpath(pathlib.Path.cwd(), args.image_folder_name))

        attachments_info = post_img_to_vk_server(server_data)
        post_img_to_group_wall(attachments_info, new_comics['comics_comment'])

    finally:
        if args.full_path_to_image:
            delete_comics(full_path_to_folder=args.full_path_to_image)
        else:
            delete_comics(folder_with_img=args.image_folder_name)
