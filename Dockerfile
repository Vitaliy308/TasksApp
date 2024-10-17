FROM python:3.11-slim
WORKDIR /app
COPY . /app/
EXPOSE 3008
ENV APP_MODE=server
CMD ["sh", "-c", "if [ \"$APP_MODE\" = \"server\" ]; then python server.py; else python client.py; fi"]
