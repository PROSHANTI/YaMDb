# Проект YaMDb

### Описание:

Проект YaMDb собирает отзывы пользователей на различные произведения.

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», 
а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 

Курс "Python-Разработчик" от Яндекс.Практикум

### Технологии:

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone https://github.com/PROSHANTI/api_yamdb.git
cd api_yamdb/
```

Cоздать и активировать виртуальное окружение:
```bash
WINDOWS:

python -m venv venv
source venv/scripts/activate

MACOS:

python3 -m venv venv
```
Установить зависимости из файла requirements.txt:
```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

Выполнить миграции:
```bash
cd api_yamdb/
python3 manage.py migrate
```

Запустить проект:
```bash
python3 manage.py runserver
```

### Примеры работы API:

После запуска проекта, документация с примерами доступна по адресу: 
```
http://127.0.0.1:8000/redoc/
```

### Авторы проекта

Максим Субботин - [GitHub](<https://github.com/PROSHANTI>)

Евгений Якимец - [GitHub](<https://github.com/gerzzog>)

Алексей Подольский - [GitHub](<https://github.com/Alexey32134>)
