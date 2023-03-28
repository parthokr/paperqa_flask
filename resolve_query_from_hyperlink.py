import os

from dotenv import load_dotenv

load_dotenv()

import requests
import uuid
from paperqa import Docs

DOWNLOAD_DIR = 'tmp'
cache = {}


def download_file(url):
    try:
        res = requests.get(url)
        path = f'{DOWNLOAD_DIR}/{uuid.uuid4()}.pdf'
        open(path, 'wb').write(res.content)
        return path
    except Exception as e:
        raise e


def fetch_answer(url, q, cleanup=True):
    global cache
    if not os.path.isdir(DOWNLOAD_DIR):
        os.mkdir(DOWNLOAD_DIR)

    try:
        docs = Docs()
        paths = []

        # lookup in cache first, otherwise download
        for each_url in url:
            if each_url in cache:
                path = cache[each_url]
            else:
                path = download_file(each_url)
            docs.add(path)
            paths.append(path)

            if not cleanup:
                cache[each_url] = path

        ans = docs.query(q)

        if cleanup:
            for path in paths:
                os.remove(path)
        return ans
    except Exception as e:
        raise e
