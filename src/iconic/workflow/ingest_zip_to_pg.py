import pandas as pd
from prefect import flow, task

from iconic.service.customer_payment import CustomerPaymentService
from iconic.service.resource import ResourceService

resource_service = ResourceService()
customer_payment_service = CustomerPaymentService()


@task
def download_test_data_zip(resource_name, destination_path):
    return resource_service.download_resource(resource_name, destination_path)


@task
def extract_test_data_zip(resource_name, downloaded_file_path, destination_path):
    extracted_file_paths = resource_service.extract_zip_resource(
        resource_name, downloaded_file_path, destination_path
    )
    data_json_file_path = [
        file_path for file_path in extracted_file_paths if file_path.endswith('data.json')
    ]

    if len(data_json_file_path) != 1:
        raise Exception

    return data_json_file_path[0]


@task
def transform_test_data_json_to_dataframe(data_json_file_path: str) -> pd.DataFrame:
    with open(data_json_file_path, 'r') as f:
        lines = f.readlines()

    # Remove EOL. Then, put comma at the end of each line, except the last line
    rows = [f'{line[:-1]},' for line in lines]
    rows[-1] = rows[-1][:-1]
    # Enclose all comma-separated json object by brackets
    json_str = '[' + ''.join(rows) + ']'

    schema = customer_payment_service.get_customer_payment_schema()
    df = pd.read_json(json_str, dtype=schema)
    df_columns = set(df.columns.tolist())
    schema_columns = set(schema.keys())
    redundant_columns = df_columns.difference(schema_columns)
    missing_columns = schema_columns.difference(df_columns)
    print(f'Redundant columns: {redundant_columns}')
    print(f'Missing columns: {missing_columns}')

    df = df.drop(columns=redundant_columns)
    df = df.drop_duplicates()
    return df


@task
def load_dataframe_into_database(df):
    customer_payment_service.upsert_df(df)


@flow(log_prints=True)
def ingest_zip_to_pg():
    source_name = 'test_data.zip'
    destination_path = '/tmp/'
    downloaded_file_path = download_test_data_zip(resource_name=source_name,
                                                  destination_path='/tmp/')
    data_json_file_path = extract_test_data_zip(resource_name=source_name,
                                                downloaded_file_path=downloaded_file_path,
                                                destination_path=destination_path)
    df = transform_test_data_json_to_dataframe(data_json_file_path)
    load_dataframe_into_database(df)


if __name__ == '__main__':
    ingest_zip_to_pg()
