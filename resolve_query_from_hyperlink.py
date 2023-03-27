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
        # lookup in cache first, otherwise download
        if url in cache:
            path = cache[url]
        else:
            path = download_file(url)

        if cleanup:
            os.remove(path)
        else:
            #  add to cache
            cache[url] = path


        docs = Docs()
        docs.add(path)
        ans = docs.query(q)


        return ans
    except Exception as e:
        raise e
