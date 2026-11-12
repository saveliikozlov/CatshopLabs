FROM python:3.12-slim

RUN useradd --create-home --uid 10001 app \
 && mkdir -p /data && chown app:app /data

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

ENV PORT=8080 PYTHONUNBUFFERED=1
USER app

EXPOSE 8080
CMD ["python", "app.py"]