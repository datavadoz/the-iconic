from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule

from iconic.workflow.report_to_business import report

# At 08:00 AM every day
deployment_daily_report = Deployment.build_from_flow(
    flow=report,
    name='daily_report',
    schedule=CronSchedule(cron="0 8 * * *", timezone="America/Chicago")
)


if __name__ == '__main__':
    deployment_daily_report.apply()
