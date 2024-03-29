# Используйте официальный образ Python
FROM python:3.10.5

# Установите рабочую директорию внутри контейнера
WORKDIR /usr/src/app

# Скопируйте файлы зависимостей и установите их
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте все файлы проекта в контейнер
COPY . .

# Укажите Docker, что контейнер слушает порт 8080 во время выполнения
EXPOSE 8080

# Укажите команду для запуска бота
CMD [ "python", "main.py" ]
