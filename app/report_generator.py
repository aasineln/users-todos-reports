import os
import logging
from typing import List
from datetime import datetime
from app.schemas import User, Tasks

logger = logging.getLogger(__name__)


class ReportClient:
    def __init__(self):
        self.reports_path = os.getenv('REPORTS_PATH', 'tasks')
        if not os.path.exists(self.reports_path):
            os.makedirs(self.reports_path)
        self.task_title_len = int(os.getenv('TASK_TITLE_LEN', 46))

    def prepare_tasks_data_to_str(self, tasks: list[str]):
        """
        Преобразует список task в одну строку для дальнейшего формирования отчетов
        """
        tasks_data = ''
        if tasks:
            for task in tasks:
                task_title = task[:self.task_title_len] + '...' if len(task) > 46 else task
                tasks_data += f'- {task_title}\n'

        return tasks_data

    def write_report(self, filename: str, data: str) -> None:
        """
        Сохраняет данные в файл, а старый переименовывает.
        Если во время формирования файла что-то пошло не так, то файл не будет создан
        :param str filename: имя файла для формирования отчета
        :param str data: данные для формирования отчета
        """
        new_file_path = os.path.join(self.reports_path, f"{filename}.txt")
        old_file_path = os.path.join(self.reports_path,
                                     f"old_{filename}_{datetime.now().strftime('%d-%m-%YT%H:%M')}.txt")

        try:
            if os.path.exists(new_file_path):
                os.rename(new_file_path, old_file_path)

            with open(new_file_path, 'w') as file:
                file.write(data)

        except Exception:
            logging.exception(f'Произошёл сбой при формировании отчета для {new_file_path}')
            if os.path.exists(old_file_path):
                os.remove(new_file_path)
                os.rename(old_file_path, new_file_path)

    def generate_report(self, user_data: User) -> None:
        """
        Формирует отчет по актуальным и выполненным задачам 1 пользователя, сохраняет отчет в формате .txt
        :param dict user_data: подготовленные данные для формирования отчета
        """
        username = user_data.username
        company = user_data.company
        email = user_data.email
        tasks = Tasks(**user_data.todos)
        active_tasks = tasks.active
        completed_tasks = tasks.completed
        report_time = datetime.now().strftime('%d.%m.%Y %H:%M')

        active_tasks_data = self.prepare_tasks_data_to_str(active_tasks)
        completed_tasks_data = self.prepare_tasks_data_to_str(completed_tasks)

        res = ''.join([
            f"# Отчёт для {company}.\n",
            f"{username} <{email}> {report_time}\n",
            f"Всего задач: {len(active_tasks) + len(completed_tasks)}\n\n",
            f"## Актуальные задачи ({len(active_tasks)}):\n",
            f'{active_tasks_data}\n',
            f"## Завершённые задачи ({len(completed_tasks)}):\n"
            f'{completed_tasks_data}\n',
        ])

        self.write_report(username, res)

    def prepare_user_todos_data(self, users: List[dict], todos: list) -> dict:
        """
        Подготавливает сырые данные о пользователях и их задачах для дальнешего формирования отчетов
        :param List[dict] users: информация о пользователях
        :param List[dict] todos: информация о задачах пользователей
        """
        logger.info('Подготовка данных о пользователях и задачах для формирования отчетов')
        res = {}

        for user in users:
            # TODO: реализовать dataclasses как в generate_report()
            user_id = user.get('id')

            if user_id:
                username = user.get('username')
                company = user.get('company').get('name')
                email = user.get('email')

                res[user_id] = {
                    "username": username,
                    "company": company,
                    "email": email,
                    "todos": {
                        "completed": [],
                        "active": []
                    }
                }

        for todo in todos:
            user_id = todo.get('userId')

            if user_id:
                title = todo.get('title')
                completed = todo.get('completed')

                if completed:
                    res[user_id]["todos"]["completed"].append(title)
                else:
                    res[user_id]["todos"]["active"].append(title)

        return res
