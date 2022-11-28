# API Yatube
## Описание.
Данный проект сделан в рамхах учебного курса Яндекс Практикум Бэкэнд-разработчик и представляет собой python telegram bot для запросов к API Яндекс. Практикум с целью проверки статуса проекта сданного на ревью

## Технологии.
Python 3.7.9,
python-telegram-bot 13.7, 
requests 2.26.0

## Установка.
Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:valliv2007/homework_bot.git
cd homework_bot
```
Cоздать и активировать виртуальное окружение:
```
python -m venv venv
source venv/Scripts/activate
```
Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
Создайте файл .env по образцу:
```
TOKEN_BOT=************************ ##  your bot's token
TOKEN_PRACTICUM=******************  ## your token which you can recieve on this site https://oauth.yandex.ru/verification_code#access_token=y0_AgAAAAABhskmAAYckQAAAADU_7oz9dzhkySnRv6JULZa3gmbLRZB41g&token_type=bearer&expires_in=2391769
MY_PHONE_ID=******** ## your phone number telegram id
```
Запустить проект:
```
python homework.py
```
