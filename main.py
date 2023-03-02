import zipfile
from getpass import getpass
from hashlib import sha256


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


if __name__ == '__main__':
    Pipeline.extract_source_data()
