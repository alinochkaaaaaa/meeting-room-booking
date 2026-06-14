FROM python:3.13-slim

WORKDIR /app

# Копируем всё приложение
COPY . .

# Устанавливаем зависимости через pip
RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    python-jose[cryptography] \
    werkzeug \
    python-dotenv \
    pydantic-settings

# Открываем порт
EXPOSE 8000

# Запускаем сервер
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]