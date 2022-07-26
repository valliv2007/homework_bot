import logging
import os
import sys
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

import exceptions

load_dotenv()


PRACTICUM_TOKEN = os.getenv('TOKEN_PRACTICUM')
TELEGRAM_TOKEN = os.getenv('TOKEN_BOT')
TELEGRAM_CHAT_ID = os.getenv('MY_PHONE_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
formater = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formater)
logger.addHandler(handler)


def send_message(bot, message):
    """Отправка сообщения ботом."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.info(
            f'Отправка сообщения "{message}" абоненту с ID:{TELEGRAM_CHAT_ID}')
    except Exception as error:
        return logging.error(f'Ошибка отправки сообщения "{message}": {error}')


def get_api_answer(current_timestamp):
    """Запрос ответа от API Практикума."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    responce = requests.get(ENDPOINT, headers=HEADERS, params=params)
    if responce.status_code != HTTPStatus.OK:
        raise exceptions.NotConnectionTOAPI(
            exceptions.NotConnectionTOAPI.__doc__)
    try:
        responce_data = responce.json()
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
    return responce_data


def check_response(response):
    """Проверка ответа от API Практикума."""
    if response == {}:
        raise exceptions.EmptyDictionary(exceptions.EmptyDictionary.__doc__)
    if type(response['homeworks']) != list:
        raise exceptions.HomeworksIsNotList(
            exceptions.HomeworksIsNotList.__doc__)
    try:
        homeworks = response['homeworks']
    except Exception as error:
        logging.error(f'Ошибка: {error}')
    return homeworks


def parse_status(homework):
    """Проверка статуса домашней работы."""
    homework_name = homework.get('homework_name')
    if homework_name is None:
        raise KeyError('Отсутсвует ключ "homework_name"')
    homework_status = homework['status']
    if homework_status not in HOMEWORK_STATUSES:
        raise exceptions.StatusIsNotExpected(
            exceptions.StatusIsNotExpected.__doc__)

    try:
        verdict = HOMEWORK_STATUSES[homework_status]
    except Exception as error:
        return logging.error(
            f'Ошибка: {error}')

    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверка переменных окружения."""
    if PRACTICUM_TOKEN and TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        return True
    else:
        logging.critical(
            'Oтсутствие обязательных переменных окружения во время запуска')
        return False


def main():
    """Основная логика работы бота."""
    if check_tokens() is False:
        raise exceptions.NotTokensInEnv(exceptions.NotTokensInEnv.__doc__)
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    send_message(bot, 'Start')
    current_timestamp = int(time.time())
    status = ''
    message = ''

    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            if homeworks != []:
                if homeworks[0].get('status') == status:
                    logging.debug('Статус работы не изменился')
                else:
                    status = homeworks[0].get('status')
                    message = parse_status(homeworks[0])
                    send_message(bot, message)
            sys.stdout
            current_timestamp = response.get('current_date')
            time.sleep(RETRY_TIME)

        except Exception as error:
            logging.error(f'Ошибка: {error}')
            new_message = f'Сбой в работе программы: {error}'
            if message != new_message:
                message = new_message
                send_message(bot, message)
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
