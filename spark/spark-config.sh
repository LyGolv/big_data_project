#!/bin/bash
. /opt/bitnami/scripts/spark/entrypoint.sh /opt/bitnami/scripts/spark/run.sh &
# wait 10s before trying to submit the job
sleep 10
# submit Python application to Spark
${SPARK_HOME}/bin/spark-submit \
      --master spark://spark:7077 \
      --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 \
      "${SPARK_HOME}/app/main.py"

