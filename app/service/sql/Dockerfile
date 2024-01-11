FROM postgres:16

WORKDIR /

ARG USE_POSTGIS=false

RUN apt-get update \
    && apt-get install -f -y --no-install-recommends \
    ca-certificates \
    software-properties-common \
    build-essential \
    pkg-config \
    git \
    postgresql-server-dev-15 \
    && add-apt-repository "deb http://ftp.debian.org/debian testing main contrib" \
    && apt-get update 