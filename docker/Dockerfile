FROM python:3.6-stretch

RUN apt-get update &&  apt-get install libjpeg-dev zlib1g-dev \
  && apt-get -yq autoremove \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Install nodejs (see: https://askubuntu.com/a/720814)
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash \
    && apt-get install nodejs \
    && apt-get -yq autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ARG VERSION

WORKDIR /app

COPY requirements.txt /tmp/
RUN pip install --upgrade pip \
    && pip install -r /tmp/requirements.txt \
    && rm -rf ~/.cache/pip

ENV ORIGIN="0.0.0.0:5100" PORT="5100" PREFIX="" LOG_LEVEL="info" BOKEH_ALLOW_WS_ORIGIN="localhost:5100"

CMD bokeh serve --port ${PORT} --address 0.0.0.0 --allow-websocket-origin ${ORIGIN} ${PREFIX_PARAM} --log-level ${LOG_LEVEL} /app --dev --show
