FROM python:3.12-slim
RUN pip install flask prometheus-flask-exporter
COPY app.py /app/app.py
COPY templates /app/templates
WORKDIR /app
ENV FLASK_APP=app.py
EXPOSE 8080
CMD ["flask","run","--host=0.0.0.0","--port=8080"]
