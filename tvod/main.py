import os
import traceback
from pathlib2 import Path
import pathlib
import configparser
import tvod.CandidateStar as cs
import tvod.StandardStar as ss
import tvod.VariableCombine as vc
import tvod.DetectVariable as dv
from aofc.aofc import AofcProcess
from PySide6.QtCore import Signal, QObject


class TvodProcess(QObject):
    sigProg = Signal(int, int, str)
    sigDebugInfo = Signal(str)
    sigError = Signal(str, str)

    def __init__(self, cat2_path=None, combine_star_path=None, save_path=None):
        super().__init__()
        self.data_filter = None
        self.ratio = None
        self.variable_star_path = None
        self.candidate_star_path = None
        self.reference_path = None
        self.combine_star_path = None
        self.cat2_path = None

        self.candidate_num = None
        self.reference_num = None
        self.p = None
        self.min_num = None

    def setParameter(self, cat2_path=None, candidate_star_path=None, combine_star_path=None, reference_path=None,
                     variable_star_path=None, candidate_num=None, reference_num=None, p=None, min_num=None,
                     data_filter=None, ratio=None):
        if cat2_path:
            self.cat2_path = cat2_path

        if candidate_star_path:
            self.candidate_star_path = candidate_star_path

        if combine_star_path:
            self.combine_star_path = combine_star_path

        if reference_path:
            self.reference_path = reference_path

        if variable_star_path:
            self.variable_star_path = variable_star_path

        if candidate_num:
            self.candidate_num = candidate_num

        if reference_num:
            self.reference_num = reference_num

        if p:
            self.p = 1 - p

        if min_num:
            self.min_num = min_num

        if ratio:
            self.ratio = ratio

        if data_filter:
            self.data_filter = data_filter

    def run(self, config_path, object_path, object_wildcard, process,
            cat2_path=None, candidate_star_path=None, combine_star_path=None, reference_path=None,
            variable_star_path=None,
            input_path=None, save_path=None, cloud_flag=None, cloud_path=None):

        path = pathlib.Path(config_path)
        # 创建实例对象
        config = configparser.ConfigParser()
        # 读取配置文件
        self.sigProg.emit(0, 1, '读取配置')
        self.sigDebugInfo.emit('读取配置...')
        config.clear()
        config.read(path, encoding="utf-8")

        candidate_num = config.get('Tvod', 'candidate_star_num')
        reference_num = config.get('Tvod', 'reference_star_num')
        p = config.get('Tvod', 'p')
        min_num = config.get('Tvod', 'min_num')
        data_filter = config.get('Tvod', 'data_filter')
        ratio = config.get('Tvod', 'ratio')
        self.sigProg.emit(1, 1, '读取配置')

        self.setParameter(cat2_path=cat2_path, combine_star_path=combine_star_path, reference_path=reference_path,
                          candidate_star_path=candidate_star_path, variable_star_path=variable_star_path,
                          candidate_num=int(candidate_num), reference_num=int(reference_num),
                          p=float(p), min_num=int(min_num), data_filter=data_filter, ratio=float(ratio))

        cat2_path = self.cat2_path
        candidate_star_path = self.candidate_star_path
        reference_path = self.reference_path
        combine_star_path = self.combine_star_path
        variable_star_path = self.variable_star_path

        candidate_num = self.candidate_num
        reference_num = self.reference_num
        p = self.p
        min_num = self.min_num
        data_filter = self.data_filter
        ratio = self.ratio

        # check dir
        if not os.path.isdir(candidate_star_path):
            os.mkdir(candidate_star_path)
        if not os.path.isdir(combine_star_path):
            os.mkdir(combine_star_path)
        if not os.path.isdir(variable_star_path):
            os.mkdir(variable_star_path)

        i = 0
        max_num = 1
        msg_error = ''
        flag_error = 0
        if 1 in process:
            max_num = max_num + 1
        if 2 in process:
            max_num = max_num + 2
        if 3 in process:
            max_num = max_num + 2

        # 预处理
        flag_error = 0
        if 1 in process:
            i = i + 1
            self.sigProg.emit(i, max_num, '数据预处理')
            self.sigDebugInfo.emit('数据预处理...')
            aofc = AofcProcess()
            flag_error, msg_error, traceback_error = aofc.run(config_path, [1,2,3,4,5,6])
            if flag_error != 0:
                self.sigProg.emit(i, i, '数据预处理失败')
                self.sigDebugInfo.emit('<font color="red">[错误]数据预处理失败</font>')
                self.sigDebugInfo.emit('<font color="red">[原因]' + msg_error + '</font>')
                self.sigError.emit(msg_error, traceback_error)
                return

        # 筛选参考星
        if 2 in process:
            flag_error = 0
            try:
                i = i + 1
                self.sigProg.emit(i, max_num, '选择候选星')
                self.sigDebugInfo.emit('选择候选星...')
                # 模块1选择候选星，ratio：参考星候选体所在区域范围，data_filter：波段，candidate_star_number：参考星候选体数量
                flag_error, error1, star_candidate_list = cs.Candidate_star(cat2_path=cat2_path,
                                                                            candidate_star_path=candidate_star_path,
                                                                            candidate_star_number=candidate_num,
                                                                            data_filter=data_filter,
                                                                            ratio=ratio)
                if flag_error != 0:
                    msg_error = ';'.join(error1)
            except Exception as e:
                msg_error = str(e)
                traceback_error = traceback.format_exc()
                self.sigError.emit(msg_error, traceback_error)
                flag_error = -1
            finally:
                if flag_error != 0:
                    self.sigProg.emit(i, i, '选择候选星失败')
                    self.sigDebugInfo.emit('<font color="red">[错误]选择候选星失败</font>')
                    self.sigDebugInfo.emit('<font color="red">[原因]' + msg_error + '</font>')
                    return
            flag_error = 0
            try:
                # 模块2筛选标准星
                i = i + 1
                self.sigProg.emit(i, max_num, '筛选标准星')
                self.sigDebugInfo.emit('筛选标准星...')
                flag_error, error2 = ss.StandardStar(candidate_star_path=candidate_star_path,
                                                     save_path=reference_path,
                                                     num=reference_num)
                if flag_error != 0:
                    msg_error = ';'.join(error2)
            except Exception as e:
                msg_error = str(e)
                traceback_error = traceback.format_exc()
                self.sigError.emit(msg_error, traceback_error)
                flag_error = -1
            finally:
                if flag_error != 0:
                    self.sigProg.emit(i, i, '筛选标准星失败')
                    self.sigDebugInfo.emit('<font color="red">[错误]筛选标准星失败</font>')
                    self.sigDebugInfo.emit('<font color="red">[原因]' + msg_error + '</font>')
                    return

        # 变源检测
        if 3 in process:
            flag_error = 0
            try:
                # 模块3遍历源
                i = i + 1
                self.sigProg.emit(i, max_num, '遍历源')
                self.sigDebugInfo.emit('遍历源...')
                cat2_path = Path(cat2_path)
                cat2_list = list(cat2_path.glob("*.cat2"))
                cat2_list.sort()
                for axx, j in enumerate(cat2_list):
                    flag_error, error3, num_write = vc.Variable_Combine(reference_path, j, combine_star_path)
                    if flag_error != 0:
                        msg_error = ';'.join(error3)
                        break
            except Exception as e:
                msg_error = str(e)
                traceback_error = traceback.format_exc()
                self.sigError.emit(msg_error, traceback_error)
                flag_error = -1
            finally:
                if flag_error != 0:
                    self.sigProg.emit(i, i, '遍历源失败')
                    self.sigDebugInfo.emit('<font color="red">[错误]遍历源失败失败</font>')
                    self.sigDebugInfo.emit('<font color="red">[原因]' + msg_error + '</font>')
                    return

            flag_error = 0
            try:
                # 识别变源
                i = i + 1
                self.sigProg.emit(i, max_num, '识别变源')
                self.sigDebugInfo.emit('识别变源...')
                ls = os.listdir(combine_star_path)
                for name in ls:
                    path_name = os.path.join(combine_star_path, name)
                    flag_error, error4, outpar = dv.Detect_variable(variable_path=path_name,
                                                                 variable_star_path=variable_star_path,
                                                                 filter_=data_filter, p_value=p, limted_num=min_num)
                    if flag_error != 0:
                        msg_error = ';'.join(error4)
                        break
            except Exception as e:
                msg_error = str(e)
                traceback_error = traceback.format_exc()
                self.sigError.emit(msg_error, traceback_error)
                flag_error = -1
            finally:
                if flag_error != 0:
                    self.sigProg.emit(i, i, '识别变源失败')
                    self.sigDebugInfo.emit('<font color="red">[错误]识别变源失败</font>')
                    self.sigDebugInfo.emit('<font color="red">[原因]' + msg_error + '</font>')
                    return

        i = i + 1
        self.sigProg.emit(i, max_num, 'Done!')
        self.sigDebugInfo.emit('<font color="green">[运行成功]</font>')
