import logging
import os
import sys
import time
from http import HTTPStatus
from typing import Any, Dict, List

import requests
import telegram
from dotenv import load_dotenv

import exceptions

load_dotenv()


PRACTICUM_TOKEN = os.getenv('TOKEN_PRACTICUM')
TELEGRAM_TOKEN = str(os.getenv('TOKEN_BOT'))
TELEGRAM_CHAT_ID = os.getenv('MY_PHONE_ID')

RETRY_TIME = 1200
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(stream=sys.stdout),
        logging.FileHandler('bot.log', encoding='UTF-8')])


def send_message(bot: telegram.bot.Bot, message: str) -> None:
    """Отправка сообщения ботом."""
    logging.info('Начало отправки сообщения ботом')
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
    except telegram.error.TelegramError as error:
        raise exceptions.NotSendMessage(
            f'Cообщение не отправлено, ошибка: {error}')
    else:
        logging.info(
            f'Отправка сообщения "{message}" абоненту с ID:{TELEGRAM_CHAT_ID}')


def get_api_answer(current_timestamp: int) -> Dict[str, Any]:
    """Запрос ответа от API Практикума."""
    logging.info('Начало запроса к  API')
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
        if response.status_code != HTTPStatus.OK:
            raise exceptions.NotConnectionTOAPI()
        response_data = response.json()
    except exceptions.NotConnectionTOAPI as error:
        raise exceptions.NotConnectionTOAPI(
            f'Ошибка подключения к API {error}, {response.status_code} '
            f'url:{ENDPOINT}, headers:{HEADERS},'f' params:{params}.')
    except Exception as error:
        raise Exception(
            f'Ошибка при запросе к основному API: {error} url:{ENDPOINT}, '
            f'headers:{HEADERS}, params:{params}.')
    return response_data


def check_response(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Проверка ответа от API Практикума."""
    logging.info('Начало проверки ответа от API')
    if not response:
        raise exceptions.EmptyDictionary('В ответе API пустой словарь.')
    if not isinstance(response['homeworks'], list):
        raise exceptions.HomeworksIsNotList(
            'Домашки приходят не в формате листа.')
    try:
        homeworks = response['homeworks']
    except KeyError as error:
        raise KeyError(f'KeyError: ключ {error} отсутсует')
    return homeworks


def parse_status(homework: Dict[str, Any]) -> str:
    """Проверка статуса домашней работы."""
    homework_name = homework.get('homework_name')
    if homework_name is None:
        raise KeyError('Отсутсвует ключ "homework_name"')
    homework_status = homework['status']
    if homework_status not in HOMEWORK_STATUSES:
        raise exceptions.StatusIsNotExpected(
            'Неожиданный статус  проверки домашки.')
    try:
        verdict = HOMEWORK_STATUSES[homework_status]
    except KeyError as error:
        raise KeyError(f'KeyError: ключ {error} отсутсует')

    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens() -> bool:
    """Проверка переменных окружения."""
    tokens = [PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID]
    return all(tokens)


def main() -> str:
    """Основная логика работы бота."""
    if check_tokens() is False:
        logging.critical(
            'Oтсутствие обязательных переменных окружения во время запуска')
        sys.exit(
            'Oтсутствие обязательных переменных окружения во время запуска')
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    prev_status = ''
    prev_time = ''
    message = ''
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            logging.debug([response, current_timestamp])
            if homeworks:
                if (homeworks[0].get('status') == prev_status
                        and homeworks[0].get('date_updated') == prev_time):
                    logging.debug('Статус работы не изменился')
                else:
                    prev_status = str(homeworks[0].get('status'))
                    prev_time = str(homeworks[0].get('date_updated'))
                    message = parse_status(homeworks[0])
                    send_message(bot, message)
            current_timestamp = int(str(response.get('current_date'))) - 1
        except exceptions.NotSendMessage as error:
            logging.error(f'Ошибка: {error}')
        except Exception as error:
            logging.error(f'Ошибка: {error}')
            new_message = f'Сбой в работе программы: {error}'
            if message != new_message:
                message = new_message
                send_message(bot, message)
        finally:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
