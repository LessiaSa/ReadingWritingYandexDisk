import os

import requests


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def upload(self, file_path: str):
        my_headers = {'Authorization': self.token}
        fname = os.path.split(file_path)[1]
        my_params = {'path': '/' + fname, 'overwrite': 'true'}
        url = 'https://cloud-api.yandex.net:443/v1/disk/resources/upload'
        r = requests.get(url, headers=my_headers, params=my_params)

        if r.status_code != requests.codes.ok:
            return f'При получении ссылки для загрузки произошла ошибка (код: {r.status_code})'

        href = r.json()['href']
        with open(file_path, 'rb') as fh:
            r = requests.put(href, data=fh.read())

        if r.status_code not in (requests.codes.created, requests.codes.accepted):
            return f'При загрузке файла произошла ошибка (код: {r.status_code})'
        return f'Файл {fname} успешно загружен на Яндекс.Диск'


if __name__ == '__main__':
    my_file_path = 'result.txt'
    auth_token = ''
    uploader = YaUploader(auth_token)
    result = uploader.upload(my_file_path)
    print(result)