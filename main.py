from api_VK import get_url_for_upload_img, post_img_to_vk_server, post_img_to_group_wall
from comics import get_comics, create_folder, save_img, delete_comics
from dotenv import load_dotenv


if __name__== '__main__':
    load_dotenv(dotenv_path='.env')
    create_folder('images')
    new_comics = get_comics()
    save_img('img', new_comics['comics_content'], 'png')
    server_data = get_url_for_upload_img()
    attachments_info = post_img_to_vk_server(server_data)
    post_img_to_group_wall(attachments_info, new_comics['comics_comment'])
    delete_comics()

