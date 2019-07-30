# Размещаем пост в Telegram-канале и группах Вконтакте и Facebook по расписанию

Модуль размещает пост в Telegram-канале и группах Вконтакте и Facebook по расписанию из Google Таблицы. 
Пост может содержать текст и картинку (фотографию) или что-то одно. 
Текст и картинки загружаются из указанных ссылок.
Формат листа `List1` в Google Таблице :

|  | A | B| C | D | E | F | G | H |
| ---------- | ---------- |-------- | ------- | --------------- | ---------------- | ------ | -------- | ------------- |
| 1 | | Соцсети |  |   |   |  |  |  |
| 2 | ВКонтакте | Телеграм | Фейсбук | День публикации | Время публикации | Статья | Картинки | Опубликовано? |
| 3 | да  | нет  | нет | вторник | 9 |  [наименование](http:// "Ссылка на статью") | [наименование](http:// "Ссылка на картинку") | нет |
| 4 | |  |  |   |   |  |  |  |

 
## Как установить
После скачивания репозитария в этой же папке создаем .env файл, в который будем добавлять необходимы строки.

#### Авторизация Google
При работе с [Google Sheets](https://developers.google.com/sheets/api/quickstart/python "https://developers.google.com/sheets/api/quickstart/python") библиотека использует специальный файл `credentials.json` с ключами и правами доступа.

Необходимо пройти авторизацию [PyDrive](https://gsuitedevs.github.io/PyDrive/docs/build/html/quickstart.html#authentication "https://gsuitedevs.github.io/PyDrive/docs/build/html/quickstart.html#authentication") и получить файл `client_secrets.json`  

Файлы с ключами кладите рядом с файлами с кодом.

#### Авторизация Вконтакте
Чтобы разместить пост на стене Вконтакте необходимо:

 - зарегистрироваться на сайте  [ВК](https://vk.com/ "https://vk.com/")
 - создать группу для размещения постов  
 - зарегистрировать приложение, которое будет размещать пост. В качестве типа приложения следует указать standalone. Новое приложение появится в списке "Мои приложения". 
 - получить `client_id` созданного приложения
 - получить [ключ доступа](https://vk.com/dev/implicit_flow_user "https://vk.com/dev/implicit_flow_user") пользователя `access_token`. Вам потребуются следующие права: photos, groups, wall и offline. 
 - скопируйте ссылку `https://vk.com/albums-{group_id}`. Замените `{group_id}` на `group_id` вашей группы. 
Создайте альбом в вашей группе и получите его `ID` ссылки `https://vk.com/album-{group_id}_{album_id}`

Необходимо добавить в .env файл:

`VK_GROUP_ID`=id вашей группы

`VK_ACCESS_TOKEN`=Ваш access_token

`VK_ALBUM_ID`=id вашего альбома в группе

#### Авторизация в Telegram-канале
Чтобы разместить пост в Telegram необходимо:

выполнить указания в статье по ссылке: [Как создать канал, бота в Телеграм](https://smmplanner.com/blog/otlozhennyj-posting-v-telegram/ "https://smmplanner.com/blog/otlozhennyj-posting-v-telegram/")

Необходимо добавить в .env файл:

`TG_ACCESS_TOKEN`=Ваш токен бота в телеграме

`TG_CHAT_ID`= Ваш идентификатор телеграмм-чата


#### Авторизация на Facebook
Чтобы разместить пост в группе Facebook необходимо:
- зарегистрироваться на сайте  [Facebook](https://www.facebook.com/ "https://www.facebook.com/")
- создать группу для размещения постов или быть администратором в существующей группе
- создать приложение в Facebook
- получить API ключ, именуемый в Facebook "маркер доступа пользователя". 
У ключа должно быть разрешение `publish_to_groups`.

Необходимо добавить в .env файл:

`FB_ACCESS_TOKEN`=Ваш токен бота в телеграме

`FB_GROUP_ID`= Ваш идентификатор группы

#### Параметры Google Таблицы

Необходимо добавить в .env файл:

`SPREADSHEET_ID` = ID Google Таблицы

`RANGE_NAME` = 'List1!A3:H'



Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:
`pip install -r requirements.txt`


Пример запуска:

`python quickstart.py `

## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/modules/ "https://dvmn.org/modules/").