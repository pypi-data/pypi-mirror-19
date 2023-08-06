import os
from contextlib import closing

import requests
from pandas import DataFrame
from tqdm import tqdm

from quantx.utils import hash
from quantx.utils.config import Config


def download(src, dst, rootdir=Config.get_cache_dir(), chunk_size=1024, label=None):
    if not os.path.isdir(rootdir):
        os.makedirs(rootdir)

    desc = "download" + "[%s]" % label if label else "download"

    dst_file = os.sep.join([rootdir, dst])
    dst_cache = os.sep.join([rootdir, hash.md5(src) + ".cache"])
    dst_len = os.path.getsize(dst_cache) if os.path.isfile(dst_cache) else 0

    with closing(requests.get(src, headers={"Range": "bytes=%d-" % dst_len}, stream=True)) as r:
        assert r.status_code == 200, "下载失败,请重试"

        with open(dst_cache, "ab") as fd:
            for chunk in tqdm(
                    r.iter_content(chunk_size),
                    desc=desc,
            ):
                fd.write(chunk)

    if os.path.isfile(dst_file):
        os.remove(dst_file)

    os.rename(dst_cache, dst_file)


def download_csv(url, label=None, chunk_size=1024, dtype=DataFrame):
    csv = hash.md5(url) + ".csv"
    download(url, csv, chunk_size=chunk_size, label=label)
    return dtype.from_csv(Config.get_cache_file(csv), index_col=None, header=0)
