FROM nvidia/cuda:11.7.1-cudnn8-runtime-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN rm /etc/apt/sources.list.d/cuda.list && \
    apt-get update && \
    apt-get install -y python3-pip python3.10 && \
    apt clean && \
    rm -rf /var/cache/apt/* && \
    rm -rf /var/lib/apt/lists/*

# PYTHONDONTWRITEBYTECODE=1: Disables the creation of .pyc files (compiled bytecode)
# PYTHONUNBUFFERED=1: Disables buffering of the standard output stream
# PYTHONIOENCODING: specifies the encoding to be used for the standard input, output, and error streams
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8

COPY requirements.txt/ /tmp/requirements.txt

RUN pip install -U pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /proj
WORKDIR /proj

RUN chmod +x /proj/scripts/start.sh
CMD ["./scripts/start.sh"]
