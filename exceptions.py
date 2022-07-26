class NotTokensInEnv(Exception):
    """Не обнаружены переменные окружения."""

    pass


class NotConnectionTOAPI(Exception):
    """Ошибка подключения к API."""

    pass


class EmptyDictionary(Exception):
    """В ответе API пустой словарь."""

    pass


class HomeworksIsNotList(Exception):
    """Домашки приходят не в формате листа."""

    pass


class StatusIsNotExpected(Exception):
    """Неожиданный статус  проверки домашки."""

    pass
