FROM python:3.10


ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8

RUN mkdir /workspace
COPY . /workspace

WORKDIR /workspace
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./src/main.py"]