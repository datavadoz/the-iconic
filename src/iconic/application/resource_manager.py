import os

import requests
from tqdm import tqdm

from iconic.service.resource import ResourceService


class ResourceManager:
    def __init__(self):
        self.resource_service = ResourceService()

    def _get_resource_url(self, resource_name):
        resource = self.resource_service.get_resource(resource_name)
        if resource is None:
            raise FileNotFoundError
        return resource.resource_url

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
