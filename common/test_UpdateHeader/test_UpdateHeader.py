# -*- coding: utf-8 -*-            
# @Author : Code_ts
# @Time : 2023/8/6 20:10

import pytest
from common import UpdateHeader as uh


class TestUpdateHeader:

    def test_01(self):
        """
        不更新文件头，所有必备关键字均存在.
        :return:
        """

        file = "test_file1.fits"
        essential_keywords = ["DEC", "RA"]
        update_keywords = {}

        try:
            r, error = uh.update_header(file, essential_keywords=essential_keywords, update_keywords=update_keywords)
            assert r == 0
        except:
            assert False

    def test_02(self):
        """
        文件不存在。
        :return:
        """
        file = "test_file2.fits"
        essential_keywords = []
        update_keywords = {}
        try:
            r, error = uh.update_header(file, essential_keywords=essential_keywords, update_keywords=update_keywords)
            assert r == 1
        except:
            assert False

    def test_03(self):
        """
        不更新文件头，必备关键字缺少一个.
        :return:
        """
        file = "test_file1.fits"
        essential_keywords = ["DEC", "RA", "AAAAAA"]
        update_keywords = {}
        try:
            r, error = uh.update_header(file, essential_keywords=essential_keywords, update_keywords=update_keywords)
            print(r)
            assert r == 3
        except:
            assert False

    def test_04(self):
        """
        缺省一个必备关键字，但是更新后，不缺省。
        :return:
        """
        file = "test_file1.fits"
        essential_keywords = ["DEC", "RA", "AAAAAA"]
        update_keywords = {"AAAAAA": "DUYU"}
        try:
            r, error = uh.update_header(file, essential_keywords=essential_keywords, update_keywords=update_keywords)
            assert r == 0
        except:
            assert False


if __name__ == "__main__":
    pytest.main()  # 添加参数可以生成报告
as