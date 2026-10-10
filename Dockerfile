FROM python:3.11-slim

LABEL maintainer="VampireDev"
LABEL description="Beastlink Audio Node"
LABEL url="https://github.com/vampirejjjadev/beastlink"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
        ffmpeg \
        curl \
        ca-certificates \
        gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY beastlink-node/ /app/

RUN pip install --no-cache-dir --upgrade beastlink pyyaml

EXPOSE 2333

CMD ["python", "beastlink_server.py"]
