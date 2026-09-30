# Dockerfile для CRM Хай-Лань
FROM python:3.12-slim

# Рабочая директория
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Открываем порт 80
EXPOSE 80

# Запуск приложения
CMD ["python", "app.py", "--host", "0.0.0.0", "--port", "80"]
