FROM prefecthq/prefect:2.8.4-python3.10

ENV ICONIC_HOME "/opt/prefect"
ENV PYTHONPATH "${PYTHONPATH}:${ICONIC_HOME}"

COPY ["src", "docker/worker/requirements.txt", "${ICONIC_HOME}"]
RUN pip install -r ${ICONIC_HOME}/requirements.txt
RUN python ${ICONIC_HOME}/iconic/deployment/deploy.py
