#!/bin/bash
. /opt/bitnami/scripts/spark/entrypoint.sh /opt/bitnami/scripts/spark/run.sh &
# wait 10s before trying to submit the job
sleep 10
# submit Python application to Spark
nohup python "${SPARK_HOME}/app/main.py"

