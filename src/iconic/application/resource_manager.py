import os
import zipfile
import requests
from tqdm import tqdm

from hashlib import sha256

from iconic.service.resource import ResourceService


class ResourceManager:
    def __init__(self):
        self.resource_service = ResourceService()

    def _get_resource_url(self, resource_name):
        resource = self.resource_service.get_resource(resource_name)
        if resource is None:
            raise FileNotFoundError
        return resource.resource_url

    def _get_resource_password(self, resource_name):
        resource = self.resource_service.get_resource(resource_name)
        if resource is None:
            raise FileNotFoundError
        return resource.resource_password

    def download_resource(self, resource_name: str, destination: str):
        url = self._get_resource_url(resource_name)
        file_path = os.path.join(destination, resource_name)

        with requests.get(url, stream=True) as stream:
            total_size_in_bytes = int(stream.headers.get('Content-Length', 0))
            block_size_in_bytes = 1024
            progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
            with open(file_path, 'wb') as file:
                for chunk in stream.iter_content(block_size_in_bytes):
                    progress_bar.set_description(f'Downloading {resource_name}...')
                    progress_bar.update(len(chunk))
                    file.write(chunk)
            progress_bar.close()

        return file_path

    def extract_zip_resource(self, resource_name, file_path, destination):
        password = self._get_resource_password(resource_name)
        encrypted_password = sha256(password.encode('utf-8')).hexdigest()

        with zipfile.ZipFile(file_path, 'r') as zip_file:
            zip_file.setpassword(bytes(encrypted_password, 'utf-8'))
            try:
                zip_file.testzip()
            except RuntimeError as e:
                print(e)
                return

            print(f'Extracting {zip_file.filename}...')
            for member in zip_file.infolist():
                print(f'\t{member.filename}: Extracting...')
                zip_file.extract(member, path=destination)
                print(f'\t{member.filename}: Done!')

        print(f'Extract {resource_name} at {destination}')
