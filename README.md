# Тестовое задание WG Forge (Backend)

Тестовое задание выполнено на языке Python 3. При выполнении задания я использовал следующие фреймворки и библиотеки:
```
 - Flask 1.0.2, основа для серверной части приложения.
 - Flask Expects JSON 1.3.1, облегчает валидацию JSON при получении POST-запроса.
 - Flask Limiter 1.0.1, устанавливает ограничения по количеству запросу.
 - Pytest 4.3.0, для написания юнит-тестов.
 - Pytest Timeout 1.3.3, устанавливает лимит по времени для выполнения тестов.
 - SQLAlchemy 1.2.14, для взаимодействия с базой данных.
```

Для запуска кода сначала скачайте репозиторий
```
git clone https://github.com/laneboi/wg_forge_backend
```

Или любым другим способом, который вы предпочитаете. В репозитории находятся следующие файлы:
```
.gitignore                  | Содержит пути к файлам, не отслеживаемым git.
application.py              | Исходный код приложения.
pytest.ini                  | Конфигурация для запуска тестов.
requirements.txt            | Необходим для удобной установки требуемых библиотек.
test_wg_forge.py            | Юнит-тесты.
wg_forge_api_exceptions.py  | Исключения, вызываемые при возникновении ошибок.
wg_forge_api_helpers.py     | Функции, дополнительно используемые API для валидации запросов.
wg_forge_api_schemas.py     | Содержит JSON-схемы для облегчения валидации POST запросов.
wg_forge_init.sql           | Инициализация базы данных.
wg_forge_task1.sql          | Решение первого задания.
wg_forge_task2.sql          | Решение второго задания.
```

Затем необходимо установить библиотеки для запуска. Находясь в консоли, используйте команду:
```
$ pip install -r requirements.txt
```

Я полагаю, что у Вас база данных уже настроена, но если я ошибаюсь, то перед проверкой придётся снова заполнить базу данных исходной информацией, а затем выполнить SQL-скрипты с решением первых двух заданий:
```
su postgres -c psql

CREATE USER wg_forge WITH PASSWORD 'a42';
CREATE DATABASE wg_forge_db_laneboi;
GRANT ALL PRIVILEGES ON DATABASE wg_forge_db TO wg_forge;

BEGIN;
\i wg_forge_init.sql
\i wg_forge_init_task1.sql
\i wg_forge_init_task2.sql
COMMIT;
```

На всякий случай в команде я изменил имя БД на "wg_forge_db_laneboi" во избежание конфликтов имён. 

Код сопровождается документацией на английском с соблюдением правил документирования Python.


# 1-е задание

Решение этого задания описано в файле wg_forge_task1.sql После выполнения скрипта и запроса
```
wg_forge_db=> SELECT * FROM cat_colors_info;
```

Получилось так:
```
        color        | count
---------------------+-------
 black               |     4
 red & black & white |     1
 black & white       |     7
 red & white         |    12
 red                 |     1
 white               |     2
(6 rows)


```


# 2-е задание

Код решения находится в wg_forge_task2.sql Решение является не полностью корректным, а именно значения tail_length_mode и whiskers_length_mode равны NULL. Эту часть задания решить не получилось. После выполнения скрипта получилось так:
```
  tail_length_mean   | tail_length_median  | tail_length_mode | whiskers_length_mean | whiskers_length_median | whiskers_length_mode
---------------------+---------------------+------------------+----------------------+------------------------+----------------------
 15.6666666666666667 | 15.0000000000000000 |                  |  12.8888888888888889 |     13.0000000000000000|
(1 row)


```

Едем дальше.

# 3-е задание

Как и просилось, здесь реализован метод ping, который на запрос:
```
curl -X GET http://localhost:8080/ping
```

будет отвечать строкой:
```
"Cats Service. Version 0.1"
```

Ничего особого в этом, к сожалению, нет. Хотя тест данного метода всё равно имеется в файле test_wg_forge.py


# 4-е задание

Теперь метод для получения списка котов. На запрос:
```
curl -X GET http://localhost:8080/cats
```

Должен возвращаться список котов в формате JSON:
```
[
  {"name": "Tihon", "color": "red & white", "tail_length": 15, "whiskers_length": 12},
  {"name": "Marfa", "color": "black & white", "tail_length": 13, "whiskers_length": 11}
]
```

Работает сортировка по заданному атрибуту, по возрастанию или убыванию:
```
curl -X GET http://localhost:8080/cats?attribute=name&order=asc
curl -X GET http://localhost:8080/cats?attribute=tail_length&order=desc
```

Так же клиент имеет возможность запросить подмножество данных, указав offset и limit:
```
curl -X GET http://localhost:8080/cats?offset=10&limit=10
```

Разумеется, клиент может указать и сортировку, и лимит одновременно:
```
curl -X GET http://localhost:8080/cats?attribute=color&order=asc&offset=5&limit=2
```

Никакие другие параметры, кроме attribute, limit, offset и order, API принимать не будет, отвечая ошибкой 400 Bad Request. Список обрабатываемых ошибок и ответов сервера на невалидный запрос с примерами описаны тут:
```
Указано слишком много атрибутов         | 400 Bad Request - The cat request takes up to 4 parameters, got 5
Указан несуществующий параметр          | 400 Bad Request - Got unexpected parameter 'spam'
Указано невалидное значение параметра*  | 400 Bad Request - Got unexpected value 'eggs' of 'offset' parameter
```

* Валидные значения параметров:
```
attribute  | name, color, tail_length, whiskers_length
limit      | all, натуральные числа. Числа с плавающей точкой невалидны
offset     | Натуральные числа. Числа с плавающей точкой невалидны. Если значение больше возможного, возвращается пустой список JSON
order      | asc, desc
```

Числа с плавающей точкой и отрицательные числа я посчитал невалидными, т.к. в случае автоматизации взаимодейтсвия с API это может указывать на ошибку в "скрипте-автоматизаторе" со стороны клиента. То же самое касается таких значений, как ascending, descending, 1, -1 параметра order.

Юнит-тесты для этого задания написаны в файле test_wg_forge.py под именами test_api_cats_case0 - test_api_cats_case6.


# 5-е задание

Запрос на добавление выглядит так:
```
curl -X POST http://localhost:8080/cat \
-d "{\"name\": \"Tihon\", \"color\": \"red & white\", \"tail_length\": 15, \"whiskers_length\": 12}"
```

Получив такой запрос сервис сохраняет в базе нового кота и отвечает клиенту сообщением "Database successfully updated." с HTTP-статусом 201 Created.

Возможные ошибки и ответы на них находятся в таблице:
```
Кот уже в базе данных               | 400 Bad Request - Cat already in database
Не JSON                             | 400 Bad Request - The browser (or proxy) sent a request that this server could not understand
Невалидный JSON                     | 400 Bad Request - The browser (or proxy) sent a request that this server could not understand
Неожиданный тип данных              | 400 Bad Request - The browser (or proxy) sent a request that this server could not understand
Отсутствует поле                    | 400 Bad Request - 'whiskers_length' is a required property
Неожиданное(ые) поле(я)             | 400 Bad Request - Got unexpected parameter(s) 'foo', 'bar', 'spam'
Отрицательная длина хвоста или усов | 400 Bad Request - 'tail_length' cannot be negative
```

Юнит-тесты для этого задания написаны в файле test_wg_forge.py под именами test_api_add_cat_case0 - test_api_add_cat_case4.


# 6-е задание


У сервиса имеется настройка, какое количество запросов он может обслужить. Допустим, это будет 600 запросов в минуту. Если количество запросов от клиентов превышает этот лимит, то часть запросов сервер отвергнет с HTTP-статусом "429 Too Many Requests".

```
curl -X GET http://localhost:8080/cats
429 Too Many Requests
```

Протестировано это банально (тест test_wg_forge.test_api_stress): отправляется 601 запрос. На первые 600 запросов ожидается статус-код 200, на 601-й статус-код 429 с сообщением об ошибке.


# Тесты


Чтобы запустить юнит-тесты, находясь в консоли запустите:
```
$ pytest test_wg_forge.py
```

Для тестов установлен лимит по времени 1.0 секунда.
