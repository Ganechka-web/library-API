# library-API

Api for social library

  

## How to set up

### Step 1, clone repository:

```

git clone https://github.com/Ganechka-web/library-API.git

```

  

### Step 2, create virtual environment and instal dependencies:

  

```

cd library-API

```

  

```

python -m venv venv

```

  

```

venv/Scripts/activate

```

  

```

pip install -r requirements.txt

```


### Step 3, setting up env varibles:

To start project?, you should fill all env varibles in `.env` file (`loc - Library-API/.env`)

```
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASS=postgres
POSTGRES_DB=postgres  

SECRET_KEY=eci&*jn3ncu2nci23n29u**(#m3u383)
ALGORITHM=HS256
```
### Step 4, starting postgreSQL in docker ccording to env varibles:

You should start docker postgres container according env varibles, you have just filled 


### Step 5, alembic migrations:

After starting postgres you need to upgrate db 

```
# Library-API/
# venv
alembic upgrade head
```

### Step 6, starting project

Type:

```
# Library-API
cd src/
```

and then

```
uvicorn main:app 
```

After this type `http://127.0.0.1:8000/docs` in browser and you will be on project docs page



## Реализация бизнес логики

В целом вся бизнес логика реализованна через слой бизнес логики к которому обращается веб-слой, далее в бизнес слое происходят проверки и конвертации данных для следующего слоя-данных

### 4.1

Данное требование выполнено с помощью передачи сервиса управления книгами в сервис по выдаче книг, далее при выдаче новой книге осуществляется попытка снизить количество существующих экземпляров, если это удалось, создаём(регистрируем) выдачу книги, в противном случае выбрасываем исключения сервисного слоя

### 4.2

Данное требование было выполнено с помощью паттерна 'валидатор', при создании экземпляра сервиса выдачи, в качестве атрибута создаётся валидатор, который применяется до создания новой выдачи. 

```python
class NoMoreThanTreeBorrowedBooksValidator:
    """validates reader`s borrowed books amount"""

    def __init__(self, repository: BorrowedBookRepository) -> None:
        self.repository = repository
  
    async def is_satisfied(self, reader_id: int):
        reader_borrowed_books = await self.repository.get_all_by_reader_id(
            reader_id=reader_id
        )
        if len(reader_borrowed_books) < 3:
            raise BorrowedBookCountPerReaderError(
                "BorrowedBook can be borrowed, "
                f"Reader with id = {reader_id} already "
                "have 3 borrowed books"
            )
```

При валидации, достаются все выданные книги по читателя и проверяется их количество

### 4.3

Для этого требования был создан метод репозитория, который достаёт выдачу книги по `id` читателя и книги, в случае отсутствия выдачи, будет возбужденно исключения сервисного слоя, также если у выдачи уже есть дата возврата будет возбужденно исключение 

```python
try:
	borrowed_book_on_return_orm = (
		await self.repository.get_one_by_reader_id_and_book_id(
			reader_id=reader_id, book_id=book_id
		)
	)
except RowDoesNotExist as e:
	raise BorrowedBookDoesNotExist(
		f"BorrowedBook with reader_id - {reader_id} "
		f"and book_id - {book_id} does not exist"
	) from e
if borrowed_book_on_return_orm.return_at is not None:
	raise BorrowedBookAlreadyReturned(
		"Unable to borrow book, already returned"
	)
```



## Структура проекта 

```
├───src
│   ├───alembic
│   │   └─── Миграци
│   ├───api
│   │   └───endpoints
│   │       └─── Эндпоинты сущностей
│   ├───core
│   │   └─── Критические файлы настроект и бд
│   ├───exceptions
│   │   └─── Файлы исключений слоёв
│   ├───models
│   │   └─── Модели SQLAlchemy
│   ├───repositories
│   │   └─── Репозитории сущностей
│   ├───schemas
│   │   └─── Pydantic схемы сущностей 
│   ├───security
│   │   └─── Файлы безопасности
│   ├───services
│   │   └─── Сервисы сущностей
```

## Структура бд

Вся структура бд была реализованна в соответствие с требованиями. Реализация выдача книги - это отдельная таблица хранящая `id` читателя и выданной книги, так как с выдачей книг была связанна основная логика, а также дополнительные поля (`borrow_at`, `return_at`) отказался от отношений один ко многим.

## Аутентификация

Механизм аутентификации представляет собой несколько последовательный этапов

1. Регистрация пользователя, хеширование введённого им пароля с помощью `passlib[bcrypc]` (выбрана из-за популярности и опыта работы с ней) 
2. Далее для получения доступа к эндпоинтам сущностей необходимо залогиниться введя электронную почту и пароль, после этого пользователя будет выдан `jwt`, который генерируется на основе `id` пользователя, секретного ключа и алгоритма, сроком на час. `python-jose` была выбрана, исключительно в личный целях, для задачи проекта достаточно было `py-jwt`.
3. При обращении к защищённым эндпоинтам токен пользователя декодируются и проверяется на достоверность (срок и существование пользователя) 

Я решил сделать все эндпоинты защищёнными, так как в тз было указанно, что всем управляет библиотекарь, следовательно, нет надобность в публичных эндпоинтах, следует допускать к управлению и просмотрю информации только доверенные лица


## Фичи

Система рекомендаций. Я бы добавил систему рекомендаций полностью подконтрольную библиотекарям, к примеру если читатель читает книги одного автора, библиотекарь может порекомендовать ему книги того же автора (к примеру отправить письмо на электронную почту). Если это было бы письмо на почту я бы использовал `fastapi-mail` и `celery` для асинхронной, фоновой отправки письма, также можно автоматизировать процесс с помшью кэша всех книг пользователя в `redis`, из них можно выбрать схожие и рекомендовать похожие каждый день с помощью `celery-beat`

