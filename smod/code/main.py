import traceback
from astropy.table import QTable
from pathlib2 import Path
import smod.code.PointClound as pc
import smod.code.Hough as hg
import smod.code.OutLines as ol
import configparser
from PySide6.QtCore import Signal, QObject

from aofc.aofc import AofcProcess


class SmodProcess(QObject):
    sigProg = Signal(int, int, str)
    sigDebugInfo = Signal(str)
    sigError = Signal(str, str)

    def __init__(self, config_path=None):
        super().__init__()

    def run(self, config_path, object_path, object_wildcard, process,
            cat2_path=None, candidate_star_path=None, combine_star_path=None, reference_path=None, variable_star_path=None,
            input_path=None, save_path=None, cloud_flag=None, cloud_path=None, track='track'):
        # 读取配置文件
        self.sigProg.emit(0, 1, '读取配置')
        self.sigDebugInfo.emit('读取配置...')
        cf = configparser.ConfigParser(converters={"raw": eval})
        cf.read(config_path, encoding='utf-8')

        image_number = int(cf.get("IdentifyTarget", "image_number"))
        p_type = cf.get("IdentifyTarget", "ptype")
        time_moment = float(cf.get("IdentifyTarget", "time_moment"))
        noise_length = float(cf.get("IdentifyTarget", "noise_length"))
        hough_npoints = int(cf.get("IdentifyTarget", "hough_npoints"))
        lines_npoints = int(cf.get("IdentifyTarget", "lines_npoints"))
        # track: str, 默认为STAR, STAR(恒星跟踪)/OBJECT(目标跟踪).
        if not track:
            track = cf.get("IdentifyTarget", "track")
        self.sigProg.emit(1, 1, '读取配置')

        aofc_flag = False
        for i in range(6):
            if i + 1 in process:
                aofc_flag = True

        flag_error = 0
        msg_error = ''
        max_num = 1
        if aofc_flag:
            max_num = max_num + 1
        if 7 in process:
            max_num = max_num + 1
        if 8 in process:
            max_num = max_num + 1
        if 9 in process:
            max_num = max_num + 2

        i = 0
        if aofc_flag:
            i = i + 1
            self.sigProg.emit(i, max_num, '数据预处理')
            self.sigDebugInfo.emit('数据预处理...')
            aofc = AofcProcess()
            flag_error, msg_error, traceback_error = aofc.run(config_path, process)
            if flag_error != 0:
                self.sigProg.emit(i, i, '数据预处理失败')
                self.sigDebugInfo.emit('<font color="red">[错误]数据预处理失败</font>')
                self.sigDebugInfo.emit('<font color="red">[原因]' + msg_error + '</font>')
                self.sigError.emit(msg_error, traceback_error)
                return

        # cat2列表，自选
        path = Path(input_path)
        cat2_list = list(path.glob("*.cat2"))

        if 7 in process:
            flag_error = 0
            try:
                # 构建点云
                if cloud_flag and cloud_path:
                    max_num = max_num + 1
                i = i + 1
                self.sigProg.emit(i, max_num, '构建点云')
                self.sigDebugInfo.emit('构建点云...')
                flag_error, error1, point_clound, point_clound_denoise, trail_time, vec = \
                    pc.read_cata(cat2_list, image_number, p_type, time_moment, noise_length)
                if flag_error != 0:
                    msg_error = ';'.join(error1)
                # 存储点云，路径自选
                if cloud_flag and cloud_path:
                    i = i + 1
                    self.sigProg.emit(i, max_num, '存储点云')
                    self.sigDebugInfo.emit('存储点云...')
                    point_clound_table = QTable.from_pandas(point_clound)
                    point_clound_table.write(cloud_path, format="ascii.fixed_width", overwrite=True)
            except Exception as e:
                msg_error = str(e)
                traceback_error = traceback.format_exc()
                self.sigError.emit(msg_error, traceback_error)
                flag_error = -1
            finally:
                if flag_error != 0:
                    self.sigProg.emit(i, i, '存储点云失败')
                    self.sigDebugInfo.emit('<font color="red">[错误]存储点云失败</font>')
                    self.sigDebugInfo.emit('<font color="red">[原因]' + msg_error + '</font>')
                    return

        if 8 in process:
            flag_error = 0
            try:
                # 霍夫变换
                i = i + 1
                self.sigProg.emit(i, max_num, '霍夫变换')
                self.sigDebugInfo.emit('霍夫变换...')
                flag_error, error2, file_lines = hg.hough(point_clound_denoise, hough_npoints)
                if flag_error:
                    msg_error = ';'.join(error2)
            except Exception as e:
                msg_error = str(e)
                traceback_error = traceback.format_exc()
                self.sigError.emit(msg_error, traceback_error)
                flag_error = -1
            finally:
                if flag_error != 0:
                    self.sigProg.emit(i, i, '霍夫变换失败')
                    self.sigDebugInfo.emit('<font color="red">[错误]霍夫变换失败</font>')
                    self.sigDebugInfo.emit('<font color="red">[原因]' + msg_error + '</font>')
                    return

        if 9 in process:
            flag_error = 0
            try:
                # 直线决策与输出
                i = i + 1
                self.sigProg.emit(i, max_num, '直线决策与输出')
                self.sigDebugInfo.emit('直线决策与输出...')
                flag_error, error3, lines_list = ol.judge_output_lines(point_clound, file_lines, trail_time, vec,
                                                                    lines_npoints, track)
                if flag_error:
                    msg_error = ';'.join(error3)
            except Exception as e:
                msg_error = str(e)
                traceback_error = traceback.format_exc()
                self.sigError.emit(msg_error, traceback_error)
                flag_error = -1
            finally:
                if flag_error != 0:
                    self.sigProg.emit(i, i, '直线决策与输出失败')
                    self.sigDebugInfo.emit('<font color="red">[错误]直线决策与输出失败</font>')
                    self.sigDebugInfo.emit('<font color="red">[原因]' + msg_error + '</font>')
                    return

            flag_error = 0
            try:
                i = i + 1
                self.sigProg.emit(i, max_num, '保存结果')
                self.sigDebugInfo.emit('保存结果...')
                fwrite_path = save_path
                ol.write_txt(save_path, lines_list, image_path=input_path)
            except Exception as e:
                msg_error = str(e)
                traceback_error = traceback.format_exc()
                self.sigError.emit(msg_error, traceback_error)
                flag_error = -1
            finally:
                if flag_error != 0:
                    self.sigProg.emit(i, i, '直线决策与输出失败')
                    self.sigDebugInfo.emit('<font color="red">[错误]直线决策与输出失败</font>')
                    self.sigDebugInfo.emit('<font color="red">[原因]' + msg_error + '</font>')
                    return

        i = i + 1
        self.sigProg.emit(i, max_num, 'Done!')
        self.sigDebugInfo.emit('<font color="green">[运行成功]</font>')
