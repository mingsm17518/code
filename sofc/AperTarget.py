# -*- coding: utf-8 -*-            
# @Author : Code_ts
# @Time : 2023/9/27 15:26

import astropy.io.fits as fits
import numpy as np
from astropy.table import Table
from pathlib2 import Path
from photutils.aperture import CircularAperture, CircularAnnulus, ApertureStats, aperture_photometry
from astropy.wcs import WCS


def aper_target(points, root_path=None, gain=None, rdnoise=None, radius=9, radius_in=12, radius_out=20, write=True):

    # points = Table.read(path, format="ascii.fixed_width").to_pandas()
    # points = points.dropna()

    points["ra"] = points["ra"].astype("float")
    points["dec"] = points["dec"].astype("float")
    points["x"] = points["x"].astype("float")
    points["y"] = points["y"].astype("float")
    points["flux"] = points["flux"].astype("float")
    points["mag"] = points["mag"].astype("float")
    points["snr"] = points["snr"].astype("float")
    points["fwhm"] = points["fwhm"].astype("float")

    col = ["id", "xcenter", "ycenter", "aperture_sum", "flux_aper", "mag", "snr_aper", "ra", "dec", "file", "time"]

    if root_path:
        root_path = Path(root_path)
    else:
        root_path = Path("./")

    for index, row in points.iterrows():
        a_fits = root_path.joinpath(row["file"])
        a_cat2 = a_fits.with_suffix(".cat2")
        print(a_fits)
        with fits.open(a_fits.as_posix()) as hduL:
            data = hduL[0].data
        with fits.open(a_cat2.as_posix()) as hduL:
            header = hduL[0].header
        a_wcs = WCS(header)

        if np.isnan(row["x"]):
            phot_data = Table()
            phot_data["id"] = [0]
            phot_data["file"] = row["file"]
            phot_data["time"] = row["time"]
            phot_data["xcenter"] = np.nan
            phot_data["ycenter"] = np.nan
            phot_data["aperture_sum"] = np.nan
            phot_data["flux_aper"]= np.nan
            phot_data["mag"] = np.nan
            phot_data["snr_aper"] = np.nan
            phot_data["mag"] = np.nan
            phot_data["ra"] = np.nan
            phot_data["dec"] = np.nan
            phot_data[col].write(a_fits.with_suffix(".aper"), format="ascii.fixed_width", overwrite=True)
            continue

        positions = (row["x"], row["y"])
        apertures = CircularAperture(positions, r=radius)
        annulus_aperture = CircularAnnulus(positions, r_in=radius_in, r_out=radius_out)
        aperstats = ApertureStats(data, annulus_aperture)
        bkg_mean = aperstats.median
        aperture_area = apertures.area_overlap(data)
        total_bkg = bkg_mean * aperture_area
        phot_data = aperture_photometry(data, apertures)
        phot_data["flux_aper"] = phot_data["aperture_sum"] - total_bkg

        if gain:
            pass
        else:
            gain = header["GAIN"]

        if rdnoise:
            pass
        else:
            rdnoise = header["RDNOISE"]

        # phot_data.rename(columns={"flux":"flux_aper"}, inpalce=True)
        # phot_data.rename_column("flux", "flux_aper")
        phot_data["snr_aper"] = (phot_data["flux_aper"] * gain) / (phot_data["aperture_sum"] * gain +
                                                              np.pi * radius * radius * rdnoise ** 2) ** 0.5
        phot_data["mag"] = 25-2.5*np.log10(phot_data["flux_aper"])
        ra, dec = a_wcs.pixel_to_world_values(phot_data["xcenter"], phot_data["ycenter"])
        phot_data["ra"] = ra
        phot_data["dec"] = dec

        phot_data["file"] = row["file"]
        phot_data["time"] = row["time"]

        phot_data["xcenter"].info.format = '.2f'
        phot_data["ycenter"].info.format = '.2f'
        phot_data["aperture_sum"].info.format = '.2f'
        phot_data["flux_aper"].info.format = '.2f'
        phot_data["mag"].info.format = '.2f'
        phot_data["snr_aper"].info.format = '.2f'
        phot_data["ra"].info.format = '.6f'
        phot_data["dec"].info.format = '.6f'

        phot_data[col].write(a_fits.with_suffix(".aper"), format="ascii.fixed_width", overwrite=True)