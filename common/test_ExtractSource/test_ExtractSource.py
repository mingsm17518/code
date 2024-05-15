# -*- coding: utf-8 -*-            
# @Author : Code_ts
# @Time : 2023/8/1 10:27

import pytest
from pathlib2 import Path
import astropy.io.fits as fits
from astropy.table import Table
from astropy.visualization import ImageNormalize, ZScaleInterval
import matplotlib.pyplot as plt


class TestES:
    def test_01(self):

        p = Path("../../datas/4613_1_1_0047720_001_0007438_6_3_20230313041919_00060_000001.calib")
        data = fits.getdata(p.as_posix())
        cata = Table.read(p.with_suffix(".cata"), format="ascii.fixed_width").to_pandas()
        streaks = cata.loc[cata["type"] == "STREAK"]
        points = cata.loc[cata["type"] == "POINT"]
        # cata1 = Table.read(p.with_suffix(".point"), format="ascii.fixed_width")
        norm = ImageNormalize(data, interval=ZScaleInterval())

        fig, ax = plt.subplots(figsize=(6, 6), dpi=300)
        ax.imshow(data, origin="lower", cmap="gray_r", norm=norm)
        ax.scatter(streaks["xcentroid"], streaks["ycentroid"], marker="o", s=100, fc=[], ec="red")
        ax.scatter(points["xcentroid"], points["ycentroid"], marker="o", s=100, fc=[], ec="green")

        plt.show()
        assert True

    def test_02(self):
        p = Path("../../datas/STARS/3C371_220416_B+N_0001.calib")
        data = fits.getdata(p.as_posix())
        cata = Table.read(p.with_suffix(".cata"), format="ascii.fixed_width").to_pandas()
        streaks = cata.loc[cata["type"] == "STREAK"]
        points = cata.loc[cata["type"] == "POINT"]
        # cata1 = Table.read(p.with_suffix(".point"), format="ascii.fixed_width")
        norm = ImageNormalize(data, interval=ZScaleInterval())

        fig, ax = plt.subplots(figsize=(6, 6), dpi=300)
        ax.imshow(data, origin="lower", cmap="gray_r", norm=norm)
        ax.scatter(streaks["xcentroid"], streaks["ycentroid"], marker="o", s=100, fc=[], ec="red")
        ax.scatter(points["xcentroid"], points["ycentroid"], marker="o", s=100, fc=[], ec="green")

        plt.show()

    def test_03(self):
        p = Path("../../datas/test1/IMG_20230316211637_SP-3_0001.fits")
        data = fits.getdata(p.as_posix())
        cata = Table.read(p.with_suffix(".cata")).to_pandas()
        streaks = cata.loc[cata["type"] == b"STREAK"]
        points = cata.loc[cata["type"] == b"POINT"]
        # cata1 = Table.read(p.with_suffix(".point"), format="ascii.fixed_width")
        norm = ImageNormalize(data, interval=ZScaleInterval())

        fig, ax = plt.subplots(figsize=(6, 6), dpi=300)
        ax.imshow(data, origin="lower", cmap="gray_r", norm=norm)
        ax.scatter(streaks["xcentroid"], streaks["ycentroid"], marker="o", s=9, fc=[], ec="red", lw=0.1)
        ax.scatter(points["xcentroid"], points["ycentroid"], marker="o", s=9, fc=[], ec="green", lw=0.1)

        plt.show()

    def test_04(self):
        p = Path("/disk16t/testdata/20230125/mst3-f02-20230125-0001.fit")
        data = fits.getdata(p.as_posix())
        cata = Table.read(p.with_suffix(".cata")).to_pandas()
        streaks = cata.loc[cata["type"] == b"STREAK"]
        points = cata.loc[cata["type"] == b"POINT"]
        # cata1 = Table.read(p.with_suffix(".point"), format="ascii.fixed_width")
        norm = ImageNormalize(data, interval=ZScaleInterval())

        fig, ax = plt.subplots(figsize=(6, 6), dpi=300)
        ax.imshow(data, origin="lower", cmap="gray_r", norm=norm)
        ax.scatter(streaks["xcentroid"], streaks["ycentroid"], marker="o", s=9, fc=[], ec="red", lw=0.1)
        ax.scatter(points["xcentroid"], points["ycentroid"], marker="o", s=9, fc=[], ec="green", lw=0.1)

        plt.show()


if __name__ == "__main__":

    pytest.main()  # 添加参数可以生成报告



