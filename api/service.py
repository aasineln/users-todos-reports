import json
import logging
import os
import requests
from requests.exceptions import ConnectionError, Timeout, HTTPError
from api.exceptions import GetUsersError, GetTodosError

logger = logging.getLogger(__name__)


class MedrocketClient:
    def __init__(self):
        self.base_url = os.getenv('MEDROCKET_BASE_URL', 'https://json.medrocket.ru')

    def _get(self, path):
        logger.info(f'Запрос к {path}')
        try:
            response = requests.get(f'{self.base_url}{path}')
            response.raise_for_status()

            if response.status_code == 200:
                return response.json()
        except ConnectionError:
            logger.error('Не удалось установить соединение')
        except Timeout:
            logger.error('Превышен таймаут запроса')
        except HTTPError as err:
            logger.error(f"Ошибка HTTP: {err}")
        except json.JSONDecodeError:
            logger.error(f"Невозможно десериализовать ответ")
        except Exception:
            logger.exception(f'Критическая ошибка при полученнии данных')

    def get_todos(self):
        path = '/todos'

        res = self._get(path)

        if not res:
            raise GetTodosError('Данные о задачах пользователей не получены!')
        return res

    def get_users(self):
        path = '/users'
        res = self._get(path)

        if not res:
            raise GetUsersError('Данные о пользователях не получены!')
        return res


