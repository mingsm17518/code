from pathlib2 import Path
import astropy.io.fits as fits
from astropy.wcs import WCS
import tqdm
import numpy as np
import itertools
import matplotlib.pyplot as plt
from astropy.visualization import ImageNormalize,ZScaleInterval

def deblendOverlap(moving_fits, fixed_fits, position=None):

    a_fits = Path(fixed_fits)
    b_fits = Path(moving_fits)

    a_data = fits.getdata(a_fits.as_posix())
    b_data = fits.getdata(b_fits.as_posix())

    a_cat2 = a_fits.with_suffix(".cat2")
    b_cat2 = b_fits.with_suffix(".cat2")

    with fits.open(a_cat2.as_posix()) as a_hduL:
        a_tab = a_hduL[1].data
        a_header = a_hduL[0].header
        a_wcs = WCS(a_header)

    with fits.open(b_cat2.as_posix()) as b_hduL:
        b_tab = b_hduL[1].data
        b_header = b_hduL[0].header
        b_wcs = WCS(b_header)


    # y_cen = a_tab["y"]
    # x_cen = a_tab["x"]
    y_cen = position[1]
    x_cen = position[0]
    x_min = x_cen - 100
    x_max = x_cen + 100
    y_min = y_cen - 100
    y_max = y_cen + 100

    b_subdata = b_data[x_min:x_max, y_min:y_max]
    x_inds = np.arange(x_min, x_max)
    y_inds = np.arange(y_min, y_max)

    a_subdata = np.zeros_like(b_data)
    aa_subdata = np.zeros_like(b_data)
    for ax,ay in tqdm.tqdm(itertools.product(x_inds, y_inds)):
        # print(ax,ay)
        ra, dec = b_wcs.pixel_to_world_values(ay, ax)
        newx, newy = a_wcs.world_to_array_index_values(ra, dec)
        xx, yy = a_wcs.all_world2pix(ra, dec, 0)
        x_ll = int(xx)
        y_ll = int(yy)
        x_lu = int(xx)
        y_lu = int(yy)+1
        x_rl = int(xx)+1
        y_rl = int(yy)
        x_ru = int(xx)+1
        y_ru = int(yy)+1

        a_subdata[ax,ay] =\
            a_data[y_ll, x_ll]*abs((x_ru-xx)*(y_ru-yy))+\
            a_data[y_lu, x_lu]*abs((x_ru-xx)*(yy-y_ll))+\
            a_data[y_rl, x_rl]*abs((xx-x_ll)*(y_ru-yy))+\
            a_data[y_ru, x_ru]*abs((xx-x_ll)*(yy-y_ll))
        aa_subdata[ax,ay] = a_data[newx, newy]


    res = b_data - a_subdata
    res1 = b_data-aa_subdata

    fig, axs = plt.subplots(3,2,figsize=(6,9), dpi=100)
    a_norm = ImageNormalize(a_data, interval=ZScaleInterval())
    b_norm = ImageNormalize(b_data, interval=ZScaleInterval())
    res_norm = ImageNormalize(res[x_min:x_max, y_min:y_max], interval=ZScaleInterval())

    axs[0,0].imshow(a_data[x_min:x_max, y_min:y_max], origin='lower', cmap='gray_r', norm=a_norm)
    axs[0,1].imshow(b_data[x_min:x_max, y_min:y_max], origin='lower', cmap='gray_r', norm=b_norm)
    axs[1,0].imshow(a_subdata[x_min:x_max, y_min:y_max], origin='lower', cmap='gray_r', norm=b_norm)
    axs[1,1].imshow(res[x_min:x_max, y_min:y_max], origin='lower', cmap='gray_r', norm=res_norm)

    axs[2,0].imshow(a_subdata[x_min:x_max, y_min:y_max], origin='lower', cmap='gray_r', norm=b_norm)
    axs[2,1].imshow(res1[x_min:x_max, y_min:y_max], origin='lower', cmap='gray_r', norm=res_norm)

    plt.savefig("deblend.png")

    # plt.show()

if __name__ == "__main__":
    b_file = Path('../datas/4613_1_1_0047720_001_0007438_6_3_20230313041919_00060_000002.fits')
    a_file = Path('../datas/4613_1_1_0047720_001_0007438_6_3_20230313041919_00060_000003.fits')
    deblendOverlap(a_file, b_file, position=(1,1))
