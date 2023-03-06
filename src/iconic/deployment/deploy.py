from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule

from iconic.workflow.report_to_business import report
from iconic.workflow.ingest_zip_to_pg import ingest_zip_to_pg


# At 08:00 AM every day
deployment_daily_report = Deployment.build_from_flow(
    flow=report,
    name='daily_report',
    schedule=CronSchedule(cron="0 8 * * *", timezone="America/Chicago"),
    work_queue_name='report',
    parameters={'receiver_email': 'danhvo.uit@gmail.com'}
)

# Run manually
deployment_ingest_zip_to_pg = Deployment.build_from_flow(
    flow=ingest_zip_to_pg,
    name='ingest_test_data',
    work_queue_name='ingest'
)


if __name__ == '__main__':
    deployment_daily_report.apply()
    deployment_ingest_zip_to_pg.apply()
