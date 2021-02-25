# -*- coding:utf-8 -*-
import json
import pytest
from sevenautotest import settings
from sevenautotest.utils import TestAssert
from sevenautotest.basetestcase import BaseTestCase
from sevenautotest.testobjects.apis.NeteaseCloudMusicApi import NeteaseCloudMusicApi


class NeteaseCloudMusicApiTest(BaseTestCase):
    """
    网易云音乐接口测试示例
    """
    def setup_class(self):

        self.api = NeteaseCloudMusicApi(settings.API_INFO[1][0])

    def setup_method(self):

        pass

    @pytest.mark.testcase("查询歌曲详情测试", author="siwenwei", editor="")
    def test_check_song_detail(self, testdata):

        song_id = testdata.get("歌曲id")
        e_name = testdata.get("预期歌曲名称")
        response = self.api.song_detail(song_id)
        res = json.loads(response.text)
        songs = res["songs"]
        song = songs[0]
        name = song["name"]
        if name != e_name:
            TestAssert.fail("%s != %s" % (name, e_name))

    @pytest.mark.testcase("查询歌手专辑测试", author="siwenwei", editor="")
    def test_get_singer_album(self, testdata):

        singer_id = testdata.get("歌手id")
        offset = testdata.get("offset")
        total = testdata.get("total")
        limit = testdata.get("limit")
        e_name = testdata.get("封面艺人名")
        response = self.api.singer_album(singer_id, offset=offset, total=total, limit=limit)
        res = json.loads(response.text)

        artist = res["artist"]
        name = artist["name"]
        if name != e_name:
            TestAssert.fail("%s != %s" % (name, e_name))

    def teardown_method(self):

        pass

    def teardown_class(self):

        pass


if __name__ == "__main__":
    pass
