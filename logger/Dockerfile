FROM python:3
WORKDIR /code
ADD ./requirements.txt .
RUN pip install -r requirements.txt
ADD . .
CMD ["python", "dalla_logger/logger_loop.py", "/run/secrets/dalla_logger_config"]