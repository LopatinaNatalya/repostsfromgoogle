import os, telegram
from dotenv import load_dotenv

class Error(Exception):
    def __init__(self, message):
        self.expression = 'Telegram-канале'
        self.message = message

    def __str__(self):
        return '{} в модуле {}.'.format(self.message, self.expression)


class FilesForPosttError(Error):
    pass


def post_image(bot, chat_id, image_filepath, caption):
    with open(image_filepath, 'rb') as photo_file:
        bot.send_photo(chat_id=chat_id, photo=photo_file, caption=caption)


def post_telegram(image_filepath=None, text_filepath=None):
    access_token = os.getenv("TG_ACCESS_TOKEN")
    chat_id = os.getenv("TG_CHAT_ID")
    bot = telegram.Bot(access_token)
    text = ''

    if image_filepath is None and text_filepath is None:
        raise FilesForPosttError('А что постим? Укажите путь до текста или картинки. Ошибка')

    if text_filepath is not None:
        with open(text_filepath, 'r', encoding="utf-8") as text_file:
            text = text_file.read()
        if image_filepath is None:
            bot.send_message(chat_id, text)

    if image_filepath is not None:
        post_image(bot, chat_id, image_filepath, text)


def main():
    load_dotenv()
    image_filepath = r'D:\files\пример для картинки.png'
    text_filepath = r'D:\files\пример для теста.txt'

    try:
        post_telegram(image_filepath, text_filepath=text_filepath)
    except FilesForPosttError as no_files_for_post:
        print(no_files_for_post)

    except FileNotFoundError as file_not_found:
        print("Файл для поста '{}' не найден.".format(file_not_found.filename))


if __name__ == "__main__":
  main()
