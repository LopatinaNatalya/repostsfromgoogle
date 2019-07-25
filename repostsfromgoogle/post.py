import argparse, post_fb, post_tg, post_vk, requests
from dotenv import load_dotenv


class Error(Exception):
    def __init__(self, message):
        self.expression = 'публикаций'
        self.message = message

    def __str__(self):
        return '{} в модуле {}.'.format(self.message, self.expression)


def post_to_social_networks(social_networks, image_filepath, text_filepath):

    if not social_networks:
        raise Error('Не указаны социальные сети')

    if 'vk' in social_networks:
        post_vk.post_vkontakte(image_filepath, text_filepath)

    if 'tg' in social_networks:
        post_tg.post_telegram(image_filepath, text_filepath)

    if 'fb' in social_networks:
        post_fb.post_facebook(image_filepath, text_filepath)


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(
       description='''Размещаем пост в Telegram-канале и группах Вконтакте и Facebook'''
    )
    parser.add_argument('--social_networks', default='vk,fb,tg',
            help='''Укажите в какие социальные сети необходимо опубликовать пост:
                            vk - будет опубликован в группе Вконтакте,
                            tg - будет опубликован в Telegram-канале,
                            fb - будет опубликован в группе Facebook,
                            если ничего не указывать - пост будет опубликован во все социальные сети''')
    parser.add_argument('--image_filepath',
            help='''Укажите путь до файла с картинкой или фотогрвфией''')
    parser.add_argument('--text_filepath',
            help='''Укажите путь до файла с текстом''')

    args = parser.parse_args()
    social_networks = args.social_networks
    image_filepath = args.image_filepath
    text_filepath = args.text_filepath

    try:
        post_to_social_networks(social_networks, image_filepath, text_filepath)

    except (post_vk.Error, post_tg.Error, post_fb.Error) as post_error:
        print(post_error)

    except FileNotFoundError as file_not_found:
        print("Файл для поста '{}' не найден.".format(file_not_found.filename))

    except requests.exceptions.ConnectionError:
        print('Отсутствует сетевое соединение')

    except requests.exceptions.ConnectTimeout:
        print('Превышено время ожидания')

if __name__ == "__main__":
  main()
