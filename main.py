import logging
from threading import Thread
from api.exceptions import GetUsersError, GetTodosError
from api.service import MedrocketClient
from app.report_generator import ReportClient
from app.schemas import User

logging.basicConfig(
    level=logging.INFO,
    filename="reports.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    logger.info('Скрипт по формированию отчетов запущен.')

    report_client = ReportClient()
    api_client = MedrocketClient()

    try:
        users = api_client.get_users()
        todos = api_client.get_todos()
    except (GetUsersError, GetTodosError):
        logging.exception('Работа скрипта завершена с ошибкой')
        return

    user_todos = report_client.prepare_user_todos_data(users, todos)

    threads = [Thread(target=report_client.generate_report, args=(User(**user_data), ))
               for user_data in user_todos.values()]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    logger.info('Скрипт по формированию отчетов завершил работу.')


if __name__ == '__main__':
    main()
