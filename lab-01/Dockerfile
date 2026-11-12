FROM python:3.12-slim AS build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim
RUN useradd --create-home --uid 10001 app \
&& mkdir -p /data && chown app:app /data
COPY --from=build /install /usr/local

WORKDIR /app
COPY app.py .
ENV PORT=8080 PYTHONUNBUFFERED=1
USER app

EXPOSE 8080
CMD ["python", "app.py"]