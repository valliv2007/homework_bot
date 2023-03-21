# Homework Bot
## Description.
This project was made as part of the Yandex.Practicum Backend Developer course and is a Python Telegram bot for requests to the Yandex API. Practicum was created to check the status of a project submitted for review.

## Technologies.
Python 3.7.9,
python-telegram-bot 13.7, 
requests 2.26.0

## Installation.
Как запустить проект:
To run the project, clone the repository and go to it in the command line:

```
git clone git@github.com:valliv2007/homework_bot.git
cd homework_bot
```
Create and activate a virtual environment:
```
python -m venv venv
source venv/Scripts/activate
```
Install dependencies from the requirements.txt file:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
Create a .env file using the sample:
```
TOKEN_BOT=************************ ##  your bot's token
TOKEN_PRACTICUM=******************  ## your token which you can recieve on this site https://oauth.yandex.ru/verification_code#access_token=y0_AgAAAAABhskmAAYckQAAAADU_7oz9dzhkySnRv6JULZa3gmbLRZB41g&token_type=bearer&expires_in=2391769
MY_PHONE_ID=******** ## your phone number telegram id
```
Run the project:
```
python homework.py
```
