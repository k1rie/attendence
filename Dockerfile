FROM python:3.11.3-alpine3.17

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache libffi-dev gcc musl-dev mariadb-connector-c-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

# fastAPI on railway
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]