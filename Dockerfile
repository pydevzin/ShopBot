FROM python:3.9.2-alpine

WORKDIR /app

COPY . /app

RUN apk update && \
    apk add --no-cache gcc musl-dev libffi-dev postgresql-dev && \
    pip install --upgrade pip && \
    pip install -r production.txt

CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000 & python main.py"]