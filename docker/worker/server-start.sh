#!/bin/bash
python ${ICONIC_HOME}/iconic/deployment/deploy.py
prefect server start --host 0.0.0.0
