FROM python:3.12-alpine

WORKDIR /app

RUN apk add --no-cache build-base git
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["sh", "-c", "gunicorn -w 4 -b 0.0.0.0:${PORT:-8000} app:app"]
