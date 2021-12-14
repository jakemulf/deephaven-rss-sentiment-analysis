FROM ghcr.io/deephaven/grpc-api
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
