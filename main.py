import zipfile
from getpass import getpass
from hashlib import sha256

import pandas as pd


class Pipeline:
    @staticmethod
    def extract_source_data():
        password = getpass('Enter password: ')
        encrypted_password = sha256(password.encode('utf-8')).hexdigest()

        with zipfile.ZipFile('data/test_data.zip', 'r') as zip_file:
            zip_file.setpassword(bytes(encrypted_password, 'utf-8'))
            try:
                zip_file.testzip()
            except RuntimeError as e:
                print(e)
                return

            print(f'Extracting {zip_file.filename}...')
            for member in zip_file.infolist():
                print(f'\t{member.filename}: Extracting...')
                zip_file.extract(member, path='data')
                print(f'\t{member.filename}: Done!')

    @staticmethod
    def clean_data():
        with open('data/data.json', 'r') as f:
            lines = f.readlines()

        rows = [f'{line[:-1]},' for line in lines]
        rows[-1] = rows[-1][:-1]
        json_str = '[' + ''.join(rows) + ']'

        schema = {
            'customer_id': str,
            'days_since_first_order': int,
            'days_since_last_order': int,
            'is_newsletter_subscriber': str,
            'orders': int,
            'items': int,
            'cancels': int,
            'returns': int,
            'different_addresses': int,
            'shipping_addresses': int,
            'devices': int,
            'vouchers': int,
            'cc_payments': int,
            'paypal_payments': int,
            'afterpay_payments': int,
            'apple_payments': int,
            'female_items': int,
            'male_items': int,
            'unisex_items': int,
            'wapp_items': int,
            'wftw_items': int,
            'mapp_items': int,
            'wacc_items': int,
            'macc_items': int,
            'mftw_items': int,
            'wspt_items': int,
            'mspt_items': int,
            'curvy_items': int,
            'sacc_items': int,
            'msite_orders': int,
            'desktop_orders': int,
            'android_orders': int,
            'ios_orders': int,
            'other_device_orders': int,
            'work_orders': int,
            'home_orders': int,
            'parcelpoint_orders': int,
            'other_collection_orders': int,
            'average_discount_onoffer': float,
            'average_discount_used': float,
            'revenue': float
        }

        df = pd.read_json(json_str, dtype=schema)
        df_columns = set(df.columns.tolist())
        schema_columns = set(schema.keys())
        redundant_columns = df_columns.difference(schema_columns)
        missing_columns = schema_columns.difference(df_columns)
        print(f'Redundant columns: {redundant_columns}')
        print(f'Missing columns: {missing_columns}')
        df = df.drop(columns=redundant_columns)
        print(df.info())


if __name__ == '__main__':
    Pipeline.extract_source_data()
    Pipeline.clean_data()
