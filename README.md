# Демо-базы для обучения PostgreSQL

В этом [видео](https://youtu.be/NFJbDist6Do) вы узнаете, как быстро развернуть популярные демо-базы данных для практики
SQL и обучения работе с PostgreSQL с помощью Docker.

Я покажу пошаговую инструкцию, как создать локальный контейнер PostgreSQL, загрузить шаблонные базы Chinook, Northwind,
Netflix и PostgresPro Demo, а также выполнить полезные SQL-запросы для анализа данных. Видео идеально подходит для
студентов, начинающих разработчиков, тех, кто готовит pet-проекты или портфолио, либо просто хочет прокачать навыки
работы с тестовыми базами.

💼 Хочешь ускорить рост в карьере? Я предлагаю менторство по дата-инженерии и IT-консультации:

- Менторство: https://korsak0v.notion.site/Data-Engineer-185c62fdf79345eb9da9928356884ea0
- Консультации: https://korsak0v.notion.site/Data-Engineer-185c62fdf79345eb9da9928356884ea0

**Что будет в ролике:**

- Быстрая установка PostgreSQL через Docker
- Загрузка и импорт учебных баз данных (Chinook, Northwind, Netflix, PostgresPro Demo)
- Примеры SQL-запросов для анализа данных
- Полезные ресурсы с другими шаблонными базами для практики

**Почему это важно:**

- Учебные базы нужны для отработки навыков SQL, тестирования запросов и подготовки к собеседованиям
- Локальная база — это быстро, бесплатно и безопасно для экспериментов

🔔 Подпишись на канал, если хочешь разбираться в реальных задачах дата-инженеров, а не только в теории.

Ссылки:

- Менторство/консультации по IT – https://korsak0v.notion.site/Data-Engineer-185c62fdf79345eb9da9928356884ea0
- TG канал – https://t.me/DataLikeQWERTY
- Instagram – https://www.instagram.com/i__korsakov/
- Habr – https://habr.com/ru/users/k0rsakov/publications/articles/
- Git-репозиторий из видео – https://github.com/k0rsakov/educational_database_for_pet_projects

## Init container

```bash
docker run -d --name my_postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -p 5432:5432 postgres:13
```

## Remove database

```bash
docker rm -f my_postgres
```

## Chinook Database

[Chinook Database](https://github.com/lerocha/chinook-database)

Копируем локально:

```bash
curl -LfO https://github.com/lerocha/chinook-database/releases/download/v1.4.5/Chinook_PostgreSql.sql
```

Выполняем скрипт в нашем контейнере:

```bash
docker exec -i my_postgres psql -U postgres -d postgres < Chinook_PostgreSql.sql
```

Пример запроса:

```sql
SELECT a2.artist_id, name, count(*)
FROM album a 
JOIN artist a2 
ON a.artist_id = a2.artist_id
WHERE 1=1
GROUP BY 1,2
ORDER BY 3 DESC
```

## Netflix Sample Database

[Netflix Sample Database](https://github.com/lerocha/netflixdb)
Копируем локально:

```bash
curl -LfO https://github.com/lerocha/netflixdb/releases/download/v1.0.11/netflixdb-postgres.zip && \
unzip netflixdb-postgres.zip && \
rm netflixdb-postgres.zip
```

Добавляем пару строк для создания БД и переключения на неё, так как в исходном скрипте такого нет:

```bash
sed -i '' '1i\
DROP DATABASE IF EXISTS netflix;\
CREATE DATABASE netflix;\
\\c netflix;\
' netflixdb-postgres.sql
```

Выполняем скрипт в нашем контейнере:

```bash
docker exec -i my_postgres psql -U postgres -d postgres < netflixdb-postgres.sql
```

Пример запроса:

```sql
SELECT m.title, sum(views)
FROM view_summary v
JOIN movie m
	ON v.movie_id = m.id
WHERE 1=1
AND m.title  = 'Minions'
AND v.duration = 'WEEKLY'
GROUP BY 1
```

## Northwind database for Postgres

[Northwind database for Postgres](https://github.com/pthom/northwind_psql)
Копируем локально:

```bash
curl -LfO https://raw.githubusercontent.com/pthom/northwind_psql/refs/heads/master/northwind.sql
```

Добавляем пару строк для создания БД и переключения на неё, так как в исходном скрипте такого нет:

```bash
sed -i '' '1i\
DROP DATABASE IF EXISTS northwind;\
CREATE DATABASE northwind;\
\\c northwind;\
' northwind.sql
```

Выполняем скрипт в нашем контейнере:

```bash
docker exec -i my_postgres psql -U postgres -d postgres < northwind.sql
```

Пример запроса:

```sql
SELECT
	e.employee_id,
	e.first_name,
	e.last_name,
	sum(price_order) AS price_order,
	sum(price_order_with_discount) AS price_order_with_discount
FROM
	orders AS o
JOIN (
		SELECT
			order_id,
			sum(unit_price * quantity) AS price_order,
			sum(unit_price * quantity *(1-discount)) AS price_order_with_discount
		FROM
			order_details
		WHERE
			1 = 1
		GROUP BY
			1
	) AS od
	ON o.order_id = od.order_id
JOIN employees AS e
	ON o.employee_id = e.employee_id
WHERE
	1=1
	AND e.city = 'London'
	AND e.title = 'Sales Representative'
GROUP BY
	1,
	2,
	3
```

## PostgresPro Demonstration Database

[PostgresPro Demonstration Database](https://postgrespro.com/community/demodb)
Копируем локально:

```bash
curl -LfO https://edu.postgrespro.com/demo-small-en.zip && \
unzip demo-small-en.zip && \
rm demo-small-en.zip
```

Выполняем скрипт в нашем контейнере:

```bash
docker exec -i my_postgres psql -U postgres -d postgres < demo-small-en-20170815.sql
```

Пример запроса:

```sql
SELECT
	departure_airport,
	count(f.arrival_airport) AS all_flights,
	count(DISTINCT arrival_airport) AS all_flights_distinct_airport
FROM flights f 	
WHERE 1=1
AND status = 'Arrived'
GROUP BY 1
ORDER BY 2 DESC
```

Курс по оптимизации
запросов – [PostgreSQL 13. Оптимизация запросов](https://www.youtube.com/playlist?list=PLaFqU3KCWw6JW80WBHPOe-SMJD2NOjmge) .

## Другие примеры баз данных

- https://github.com/oracle-samples/db-sample-schemas/tree/main
- https://github.com/microsoft/sql-server-samples
- https://github.com/datacharmer/test_db

[YouTube видео с демонстрацией баз данных для обучения PostgreSQL](https://youtu.be/NFJbDist6Do)