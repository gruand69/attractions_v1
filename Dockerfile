# Создать образ на основе базового слоя,
# который содержит файлы ОС и интерпретатор Python 3.9.
FROM python:3.10.12

WORKDIR /app

RUN pip install gunicorn==20.1.0

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

WORKDIR attractions

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "attractions.wsgi"]