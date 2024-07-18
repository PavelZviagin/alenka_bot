# Используем официальный образ Python в качестве базового
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /usr/src/app

# Установка зависимостей для сборки
RUN apt-get update && \
    apt-get install -y gcc libpq-dev

# Копируем файл requirements.txt и устанавливаем зависимости
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем оставшиеся файлы проекта
COPY . .

# Определяем команду запуска
CMD ["python", "main.py"]