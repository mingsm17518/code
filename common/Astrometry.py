import os
from pathlib2 import Path
import astropy.io.fits as fits
import time
import subprocess


# 定义一个函数，防止出现坐标“12 34 56”的情况
def dms_to_degrees(dms_string):
    dms_parts = dms_string.split()  # 将字符串分割为度、分、秒的部分
    degrees = float(dms_parts[0])  # 度部分直接转换为浮点数

    if len(dms_parts) > 1:
        minutes = float(dms_parts[1])
        degrees += minutes / 60.0  # 将分转换为度并加到总度数上

    if len(dms_parts) > 2:
        seconds = float(dms_parts[2])
        degrees += seconds / 3600.0  # 将秒转换为度并加到总度数上

    return degrees


def astrometry(xyls: str, wcs_output: str = None):
    """
    天文定位,函数生成wcs文件(*.wcs)
    :param para:xyls-xy列表绝对路径名+文件名(str)
    :param para:wcs_output-输出的wcs文件的名字与位置，以绝对路径名+文件名的方式提供(str)

    :return:错误码
            0-"参数必须是字符串类型"
            1-"未运行成功，星像列表未提供"
            2-"未运行成功，星像列表文件格式错误"
            3-"未运行成功，wcs输出地址错误"
            4-"未运行成功，NAXIS关键字错误或未提供"
            5-"未运行成功，未找到wcs文件"
    :return:error_lst-错误列表,以字符串格式记录了程序运行时出现的问题
    :return:wcs-生成的wcs文件的绝对路径名+文件名(str)
    """
    # 错误列表
    error_lst = []

    # 检查参数输入格式
    if xyls is not None and not isinstance(xyls, str):
        error_lst.append("参数必须是字符串类型")
        return 1, error_lst, None
    if wcs_output is not None and not isinstance(wcs_output, str):
        error_lst.append("参数必须是字符串类型")
        return 1, error_lst, None

    # 检查输入文件
    try:
        hdu = fits.open(Path(xyls))
        header = hdu[0].header
    except FileNotFoundError:
        error_lst.append("未运行成功，星像列表未提供")
        return 2, error_lst, None
    except:
        error_lst.append("未运行成功，星像列表文件格式错误")
        return 3, error_lst, None

    # 检查wcs_output参数
    if wcs_output is None:
        wcs = Path(xyls).with_suffix(".wcs")
    else:
        try:
            wcs = Path(wcs_output).with_suffix(".wcs")
        except:
            error_lst.append("未运行成功，wcs输出地址错误")
            return 4, error_lst, None

    str1 = "solve-field "
    str2 = " --depth 20,30,40,50,60,70,80,90,100 "
    str3 = "--corr none "
    str4 = "--index-xyls none "
    str5 = "--match none "
    sl = Path(xyls).with_suffix(".solve")
    str6 = f"--solved {sl} "
    str7 = "--rdls none "
    str8 = "-O "
    try:
        scale_min = header["SCALE"] - 0.1
        scale_max = header["SCALE"] + 0.1
        str9 = f"--scale-units arcsecperpix --scale-low {scale_min} "
        str10 = f"--scale-high {scale_max} "
    except:
        str9 = ""
        str10 = ""
        # error_lst.append("未给定像元比例尺,可能导致定位速度变慢")
    str11 = "-p "

    try:
        if header["CRVAL1"] != 0:
            ra = header["CRVAL1"]
            dec = header["CRVAL2"]
            str12 = f"--ra {ra} --dec {dec} --radius 2 "
        else:
            # ra = header["CRVAL1"]
            # dec = header["CRVAL2"]
            str12 = ""
    except ValueError:
        ra = dms_to_degrees(header["CRVAL1"])
        dec = dms_to_degrees(header["CRVAL2"])
        str12 = f"--ra {ra} --dec {dec} --radius 2 "
    except:
        str12 = ""
        # error_lst.append("未给定图像指向坐标,可能导致定位速度变慢")
    str13 = "--x-column xcentroid --y-column ycentroid "
    str14 = "--sort-column segment_flux "
    try:
        N1 = header["XSIZE"]
        N2 = header["YSIZE"]
        str15 = f"--width {N1} --height {N2} "
    except:
        error_lst.append("未运行成功，NAXIS关键字错误或未提供")
        return 5, error_lst, None
    str16 = f"{xyls} "
    str17 = "-c 0.01 -O -t 3 --crpix-center "
    str18 = "--no-plots --no-remove-lines --uniformize 0 "
    str19 = f"--wcs {str(wcs)} "

    cmd = str1 + str2 + str3 + str4 + str5 + str6 + str7 + str8 + str9 + \
          str10 + str11 + str12 + str13 + str14 + str15 + str16 + str17 + str18 + str19

    try:
        output = run_command(cmd)
        # print("输出信息：", output)
    except Exception as e:
        raise e

    try:
        hdu_wcs = fits.getheader(wcs)
    except:
        error_lst.append("未运行成功，未找到wcs文件")
        return 6, error_lst, None

    # 检测并删除中间文件
    while True:
        if os.path.exists(str(sl)):
            axy = Path(xyls).with_suffix(".axy")
            os.remove(str(axy))
            try:
                hdu_wcs = fits.getheader(wcs)
            except:
                error_lst.append("未运行成功，未找到wcs文件")
                return 7, error_lst, None
            # 必须保留的关键字列表
            essential_keywords = ["NAXIS", "BITPIX", "SIMPLE", "EXTEND"]
            for keyword in hdu_wcs:
                if keyword in header and keyword not in essential_keywords:
                    del header[keyword]
            header.extend(hdu_wcs, end=True)
            hdu.writeto(Path(xyls).with_suffix('.cat1'), overwrite=True)
            try:
                os.remove(str(sl))
                # os.remove(str(wcs))
            except:
                break

            break  # 文件找到，退出循环并返回True
        start_time = time.time()  # 获取当前时间
        # 如果经过了10秒），则中断循环并返回False
        if time.time() - start_time > 10:
            break
        time.sleep(0.1)  # 每次等待0.1秒后再次检测

    return 0, [], str(wcs)


def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if process.returncode != 0:
        raise Exception("命令执行失败，错误信息：" + error.decode('utf-8'))
    return output.decode('utf-8')

# if __name__ == "__main__":

#     xyls = "/dsk16t/s05/xgd/t7/3C371_220416_B+N_0001.cat"
#     a=astrometry(xyls)
#     print(a)
