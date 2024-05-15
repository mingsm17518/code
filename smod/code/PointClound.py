import os
import uuid
import warnings
import numpy as np
import pandas as pd
from astropy.wcs import WCS
import astropy.io.fits as fits
from astropy.table import Table
warnings.filterwarnings("ignore")
import astropy.wcs.utils as utils
from astropy.coordinates import SkyCoord

def read_cata(cata_list, number = 4, p_type = "POINT", moment = 20, noise_length = 2):
    """
    构建点云
    :param cata_list: list，必备，星像列表与WCS信息.
    :param number: int，默认为4，图像最少数量.
    :param p_type: str，默认为POINT(点星像)，星像类型(STREAK(拖长)/POINT(点)/ALL(点/拖长)).
    :param moment: float，默认为20，图像间间隔.
    :param noise_length: float，默认为2，点云降噪像素间隔.
    :return: status:状态码；error_lst:运行异常信息；point_clound:原始点云；point_clound_denoise:降噪点云; trail_time:时间尺寸; vec:图像速度.
    """
    #错误信息
    error_lst=[]
    
    #文件列表
    cata_list.sort()
    
    #星像列表数量少于number，报错
    if len(cata_list) < number:
        error_lst.append(".cat2文件数量少于"+str(number))
        point_clound = None
        point_clound_denoise = None
        trail_time = None
        vec = None
        return 1, error_lst, point_clound, point_clound_denoise, trail_time, vec
    
    #读取星像信息
    x,y,time,ra,dec,snr,fwhm,file,ptype,flux,mag = [],[],[],[],[],[],[],[],[],[],[]
    cata_columns = ["xcentroid", "ycentroid", "JD", "snr_aper", "fwhm", "file", \
                    "type", "ra", "dec", "flux_aper", "mag_aper"]
    for i in range(len(cata_list)):
        a_cata = cata_list[i]
        
        cata = fits.open(a_cata)
        temp = Table(cata[1].data)
        columns_dif = list(set(cata_columns).difference(set(list(temp.columns))))
        if len(columns_dif) > 0:
            para = ":"
            for a_para in columns_dif:
                para = para + a_para + " "
            error_lst.append(".cat2缺少参数"+para)
            point_clound = None
            point_clound_denoise = None
            trail_time = None
            vec = None
            return 2, error_lst, point_clound, point_clound_denoise, trail_time, vec

        x = x+list(temp["xcentroid"])
        y = y+list(temp["ycentroid"])
        ra = ra+list(temp["ra"])
        dec = dec+list(temp["dec"])
        time = time+list(temp["JD"])
        snr = snr+list(temp["snr_aper"])
        fwhm = fwhm+list(temp["fwhm"])
        file = file+list(temp["file"])
        ptype = ptype+list(temp["type"])
        flux = flux+list(temp["flux_aper"])
        mag = mag+list(temp["mag_aper"])
            
            
    point_clound = pd.DataFrame({"ra":ra, "dec":dec, "x":x, "y":y, "snr":snr, "fwhm":fwhm, \
                                 "file":file, "time":time, "ptype":ptype, "flux":flux, "mag":mag})
    
    #点云坐标对齐
    cata_mid = fits.open(cata_list[int(len(cata_list)/2)])
    wcs_mid = WCS(cata_mid[0].header)
    skycoord = SkyCoord(point_clound["ra"], point_clound["dec"], frame="icrs", unit="deg")
    point_clound["xcen"],point_clound["ycen"] = utils.skycoord_to_pixel(skycoord,wcs_mid,origin=0)
    
    
    #变换时间
    Tt = list(np.unique(point_clound.time))
    Tt.sort()
    T_diff = [Tt[i+1]-Tt[i] for i in range(len(Tt)-1)]
    T_scale = moment/(min(T_diff)*24*3600)
    point_clound["zcen"] = (point_clound["time"] - Tt[0])*24*3600*T_scale
    
    #望远镜速度
    Tt = list(np.unique(point_clound.zcen))
    Tt.sort()
    naxis1 = cata_mid[0].header['XSIZE']
    naxis2 = cata_mid[0].header['YSIZE']
    exposure = cata_mid[0].header['EXPTIME']
    
    trail_time = T_scale*exposure
    cata_first = fits.open(cata_list[0])
    wcs_first = WCS(cata_first[0].header)
    cata_last = fits.open(cata_list[-1])
    wcs_last = WCS(cata_last[0].header)
    reference_x = naxis1/2
    reference_y = naxis2/2
    reference_sky = utils.pixel_to_skycoord(reference_x,reference_y,wcs_first,origin=1)
    reference_x1,reference_y1 = utils.skycoord_to_pixel(reference_sky,wcs_last,origin=0)
    if reference_x1 >= reference_x:
        vec = np.array([reference_x1-reference_x, reference_y1-reference_y, Tt[-1]-Tt[0]])
    else:
        vec = np.array([reference_x-reference_x1, reference_y-reference_y1, Tt[0]-Tt[-1]])
    vec = vec*(trail_time/vec[2])
    
    #保存点云
    point_clound = point_clound.sort_values(by = ["zcen","xcen","ycen"])
    if p_type == 'ALL':
        point_clound = point_clound
    else:
        point_clound = point_clound[point_clound.ptype == p_type]
    
    #降噪
    point_clound["xcen_int"] = (point_clound["xcen"]/noise_length).astype(int)
    point_clound["ycen_int"] = (point_clound["ycen"]/noise_length).astype(int)
    point_clound_denoise = point_clound.drop_duplicates(subset = ["xcen_int", "ycen_int"], keep = False)
    point_clound_denoise = point_clound_denoise[["xcen","ycen","zcen"]]
    
    #点云中点数量太多，报错
    if len(point_clound_denoise) >= 100000:
        error_lst.append("点云中点数量太多，建议加大noise_length")
        return 3, error_lst, point_clound, point_clound_denoise, trail_time, vec
    
    return 0, error_lst, point_clound, point_clound_denoise, trail_time, vec