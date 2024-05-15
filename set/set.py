# -*- coding: utf-8 -*-
# @Author : Code_ts
# @Time : 2023/8/16 18:50

import configparser
import sys
import traceback
from pathlib2 import Path
from astropy.table import Table, vstack

sys.path.append(".")
import common.UpdateHeader as uph
# import common.ExtractSource as sex
import tqdm
import common.PreProcess as pp
from common.Astrometry import astrometry
# from common.Calibration import calibration
import sofc.IdentifyTarget as it
import sofc.AperTarget as at
import smod.code.OutLines as ol

from PySide6.QtCore import Signal, QObject


class SetProcess(QObject):
    def __init__(self, config_path=None):
        super().__init__()
        self.config_path = config_path

    def setConfigPath(self, config_path=None):
        self.config_path = config_path
