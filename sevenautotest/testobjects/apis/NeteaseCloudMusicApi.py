# -*- coding: utf-8 -*-
import requests
from urllib.parse import urljoin
from sevenautotest.utils.DataProvider import DataProvider as data_provider

__version__ = "1.0"
__author__ = "si wen wei"


class NeteaseCloudMusicApi(object):
    """网易云音乐接口封装"""
    def __init__(self, url):
        self.url = url

    @data_provider()
    def song_detail(self, apidata, song_id):
        """歌曲信息"""

        api_path = apidata.get("接口路径")
        payload = {"id": song_id, "ids": "[{}]".format(song_id)}
        res = requests.get(url=urljoin(self.url, api_path), params=payload)
        return res

    @data_provider()
    def singer_album(self, apidata, singer_id, offset=0, total=True, limit=5):
        """歌手专辑"""

        api_path = apidata.get("接口路径")
        full_path = urljoin(self.url, api_path)
        payload = {"id": singer_id, "offset": offset, "total": total, "limit": limit}
        res = requests.get(url=urljoin(full_path, singer_id), params=payload)
        return res
