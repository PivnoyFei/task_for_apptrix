[![Build Status](https://github.com/PivnoyFei/task_for_apptrix/actions/workflows/apptrix_actions.yml/badge.svg)](https://github.com/PivnoyFei/task_for_apptrix/actions/workflows/apptrix_actions.yml)

<h1 align="center"><a target="_blank" href="">Тестовое для Apptrix</a></h1>

### Стек: 
![Python](https://img.shields.io/badge/Python-171515?style=flat-square&logo=Python)![3.11](https://img.shields.io/badge/3.11-blue?style=flat-square&logo=3.11)
![Django](https://img.shields.io/badge/Django-171515?style=flat-square&logo=Django)![4.2.2](https://img.shields.io/badge/4.2.2-blue?style=flat-square&logo=0.96.0)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-171515?style=flat-square&logo=PostgreSQL)![13.0](https://img.shields.io/badge/14.6-blue?style=flat-square&logo=13.0)
![Docker-compose](https://img.shields.io/badge/Docker--compose-171515?style=flat-square&logo=Docker)


### Общая идея: 
пишем бекэнд для сайта (приложения) знакомств.
### Как работаем:
#### Каждый пункт задачи - отдельный коммит. После выполнения каждого пункта пушим коммит в проект:
#### git add .
#### git commit -m "Сделал то-то и то-то"
#### git push origin {ветка}
#### После завершения ссылку на все коммиты кидаем в общий чат.
### Задачи:
1. Создать модель участников. У участника должна быть аватарка, пол, имя и фамилия, почта.
2. Создать эндпоинт регистрации нового участника: /api/clients/create (не забываем о пароле и совместимости с авторизацией модели участника).
3. При регистрации нового участника необходимо обработать его аватарку: наложить на него водяной знак (в качестве водяного знака можете взять любую картинку).
4. Создать эндпоинт оценивания участником другого участника: /api/clients/{id}/match. В случае, если возникает взаимная симпатия, то ответом выдаем почту клиенту и отправляем на почты участников: «Вы понравились <имя>! Почта участника: <почта>».
5. Создать эндпоинт списка участников: /api/list. Должна быть возможность фильтрации списка по полу, имени, фамилии. Советую использовать библиотеку Django-filters.
6. Реализовать определение дистанции между участниками. Добавить поля долготы и широты. В api списка добавить дополнительный фильтр, который показывает участников в пределах заданной дистанции относительно авторизованного пользователя. Не забывайте об оптимизации запросов к базе данных
https://en.wikipedia.org/wiki/Great-circle_distance
7. Задеплоить проект на любом удобном для вас хостинге, сервисах PaaS (Heroku) и т.п. Должна быть возможность просмотреть реализацию всех задач. Если есть какие-то особенности по тестированию, написать в Readme. Там же оставить ссылку/ссылки на АПИ проекта
### Приветствуется:
1. Аккуратный код
2. Соблюдение PEP8 (Pycodestyle)



### Запуск проекта
Клонируем репозиторий и переходим в него:
```bash
git clone https://github.com/PivnoyFei/task_for_apptrix.git
cd task_for_apptrix
cd apptrix-infra
```

### Запуск проекта c SQLite
```bash
docker compose -f docker-compose.override.yml up -d --build
```

### Перед запуском сервера c PostgreSQL, в папке infra необходимо создать .env файл, с такими же ключами как и .env.template но со своими значениями.
```bash
docker-compose up -d --build
```

#### Миграции базы данных:
```bash
docker-compose exec apptrix-backend python manage.py makemigrations
docker-compose exec apptrix-backend python manage.py migrate --noinput
```
```bash
docker-compose exec apptrix-backend python manage.py collectstatic --noinput
docker-compose exec apptrix-backend python manage.py createsuperuser
```

#### Останавливаем контейнеры:
```bash
docker-compose down -v
```

#### Автор
[Смелов Илья](https://github.com/PivnoyFei)
