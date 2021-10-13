FROM python:3.9-slim-bullseye

# Install security updates.
RUN --mount=type=cache,target=/var/cache/apt,id=apt \
    apt-get update -q && \
    DEBIAN_FRONTEND=noninteractive apt-get -y upgrade && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache,id=pip \
    python3 -m venv --system-site-packages --without-pip /opt/venv && \
    /opt/venv/bin/python3 -m pip install -r requirements.txt
ENV PATH=/opt/venv/bin:$PATH

COPY . .

VOLUME ["/episodes"]
WORKDIR /episodes

ENTRYPOINT ["/app/shortwave.py"]
