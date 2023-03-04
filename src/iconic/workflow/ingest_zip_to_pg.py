from prefect import flow, task, get_run_logger

from iconic.application.resource_manager import ResourceManager


@task
def download_resource(resource_name, destination):
    logger = get_run_logger()
    file_path = resource_manager.download_resource(resource_name, destination)
    logger.info(f'Downloaded {resource_name} at {file_path}')
    return file_path


@flow
def ingest_zip_to_pg():
    file_path = download_resource('test_data.zip', '/tmp/')
    print(file_path)


if __name__ == '__main__':
    resource_manager = ResourceManager()
    ingest_zip_to_pg()
