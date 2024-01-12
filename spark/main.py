import datetime
import logging

from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_spark_submit():
    spark_home="/opt/bitnami/spark"
    subprocess.run([
        f'{spark_home}/bin/spark-submit',
        '--master', 'spark://spark:7077',
        '--packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0',
        '--jars', '/opt/bitnami/spark/jars/postgresql-42.7.1.jar',
        f'{spark_home}/app/analyse_trending_videos.py'
    ])


# Create a scheduler
scheduler = BlockingScheduler()

# Schedule the spark-submit command every 15 minutes
scheduler.add_job(run_spark_submit, 'interval', minutes=3)

try:
    # Start the scheduler
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    # Gracefully exit on KeyboardInterrupt or SystemExit
    pass
