FROM python:3.11-slim
WORKDIR /app
COPY . /app/
EXPOSE 3008
CMD ["python", "server.py"]
