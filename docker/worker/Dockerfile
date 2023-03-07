FROM prefecthq/prefect:2.8.4-python3.10

ENV ICONIC_HOME "/opt/prefect"
ENV PYTHONPATH "${PYTHONPATH}:${ICONIC_HOME}"

COPY ["docker/worker/requirements.txt", "docker/worker/server-start.sh", "${ICONIC_HOME}"]
RUN pip install -r ${ICONIC_HOME}/requirements.txt

COPY ["src", "${ICONIC_HOME}"]
