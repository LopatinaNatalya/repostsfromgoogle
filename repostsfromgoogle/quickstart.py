from __future__ import print_function
import pickle, os.path, datetime, re, requests, time
import post, post_vk, post_fb, post_tg
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_credentials():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def get_id(text):
    return re.findall(r'id=.[^"]+',text)[0][3:]


def get_article(id, drive):
    mimetype = 'text/plain'

    file = drive.CreateFile({'id': id})

    title = '{}.{}'.format(file['title'], 'txt')
    file.GetContentFile(title, mimetype=mimetype)
    return title


def get_image(id, drive):
    file = drive.CreateFile({'id': id})
    title = file['title']

    file.GetContentFile(title) # Download file as 'catlove.png'.
    return title


def publish_articles(last_attempt_timestamp):
    spreadsheet_id = os.getenv("SPREADSHEET_ID")
    range_name = os.getenv('RANGE_NAME')
    value_render_option = 'FORMULA'
    value_input_option = 'USER_ENTERED'
    weekdays = {
        'понедельник': 0,
        'вторник': 1,
        'среда': 2,
        'четверг': 3,
        'пятница': 4,
        'суббота': 5,
        'воскресенье': 6,
        }

    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range=range_name,
                                valueRenderOption=value_render_option
                                ).execute()

    values = result.get('values', [])

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    for row in values:
        if str(row[7]).upper() == 'ДА':
            continue

        post_weekday = weekdays.get(row[3], None)
        today_weekday = datetime.date.today().weekday()
        if post_weekday is None or post_weekday !=  today_weekday:
            continue

        post_hour = row[4]
        if not float(post_hour).is_integer():
            continue

        now = datetime.datetime.now()
        post_datetime = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=int(post_hour)).timestamp()
        if post_datetime <=  last_attempt_timestamp or post_datetime >= now.timestamp():
            continue

        text_filepath = get_article(get_id(row[5]), drive)
        image_filepath = get_image(get_id(row[6]), drive)
        social_networks = ''
        if str(row[0]).upper() == 'ДА':
            social_networks += 'vk,'

        if str(row[1]).upper() == 'ДА':
            social_networks += 'tg,'

        if str(row[2]).upper() == 'ДА':
            social_networks += 'fb'

        post.post_to_social_networks(social_networks, image_filepath, text_filepath)
        row[7] = 'да'

        os.remove(text_filepath)
        os.remove(image_filepath)

    body = {
        'values': values
    }

    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption=value_input_option, body=body).execute()


def main():
    load_dotenv()
    last_attempt_timestamp = (datetime.datetime.now()- datetime.timedelta(hours=1)).timestamp()

    for i in range(1):
        try:
            publish_articles(last_attempt_timestamp)

        except (post_vk.Error, post_tg.Error, post_fb.Error, post.Error) as post_error:
            print(post_error)
            break

        except FileNotFoundError as file_not_found:
            print("Файл для поста '{}' не найден.".format(file_not_found.filename))
            break

        except requests.exceptions.ConnectionError:
            print('Отсутствует сетевое соединение')

        except requests.exceptions.ConnectTimeout:
            print('Превышено время ожидания')

        last_attempt_timestamp = datetime.datetime.now().timestamp()

        time.sleep(1800)


if __name__ == '__main__':
    main()

