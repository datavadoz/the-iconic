FROM prefecthq/prefect:2.8.4-python3.10

COPY ["docker/worker/requirements.txt", "/opt/prefect"]

ENV PYTHONPATH "${PYTHONPATH}:/opt/prefect/src"

RUN pip install -r /opt/prefect/requirements.txt
