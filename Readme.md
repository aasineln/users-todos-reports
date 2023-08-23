## Формирование отчетов о выполненных и актуальных задачах пользователей  
Данный скрипт получает список задач (todos) и список пользователей (users) от API:  
https://json.medrocket.ru/todos  
https://json.medrocket.ru/users  
Составляет отчёты по всем пользователям в отдельных текстовых файлах в формате .txt.
Полное ТЗ находится в файле task.md.
  
### Пример отчета  
```  
# Отчёт для Deckow-Crist.  
Ervin Howell <Shanna@melissa.tv> 23.09.2020 15:25  
Всего задач: 4  
  
## Актуальные задачи (2):  
- suscipit repellat esse quibusdam voluptatem in…  
- laborum aut in quam  
  
## Завершённые задачи (2):  
- distinctio vitae autem nihil ut molestias quo  
- est ut voluptate quam dolor  
```  
  
  ### Запуск скрипта
  Необходимо переименовать:
```
$ make setup
$ make run
``` 
