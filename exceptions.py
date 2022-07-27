class NotConnectionTOAPI(Exception):
    """Ошибка подключения к API."""


class EmptyDictionary(Exception):
    """В ответе API пустой словарь."""


class HomeworksIsNotList(Exception):
    """Домашки приходят не в формате листа."""


class StatusIsNotExpected(Exception):
    """Неожиданный статус  проверки домашки."""


class NotSendMessage(Exception):
    """Cообщение не отправлено."""
