from prefect import flow, task

from iconic.application.resource_manager import ResourceManager


@task
def download_resource(resource_name, destination):
    file_path = resource_manager.download_resource(resource_name, destination)
    print(f'Downloaded {resource_name} at {file_path}')
    return file_path


@task
def extract_resource(resource_name, file_path, destination):
    resource_manager.extract_zip_resource(resource_name, file_path, destination)


@flow(log_prints=True)
def ingest_zip_to_pg():
    resource_name = 'test_data.zip'
    destination_path = '/tmp/'
    file_path = download_resource(resource_name, destination_path)
    extract_resource(resource_name, file_path, destination_path)


if __name__ == '__main__':
    resource_manager = ResourceManager()
    ingest_zip_to_pg()
