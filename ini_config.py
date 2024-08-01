# -*- coding: utf-8 -*-


# 文档字符串
"""ini配置文件控制
日常使用是保存在内存中
需要调用函数保存到文件
"""


# 模块级的“呆”名
__all__ = ['IniConfig', 'GlobalConfig'] # 模块名称列表
__version__ = '0.1'
__author__ = 'lihua.tan'


# 基础库
import os# 操作系统库
import sys# 系统
from enum import IntEnum# 枚举
from configparser import ConfigParser# 配置解析库
# 自封装库
pass


# 配置键名索引
class ConfigKey(IntEnum):
    """配置键名索引
    """
    UpdateLevelCount = 0


# 全局ini配置文件控制
class GlobalConfig(object):
    '''全局ini配置文件控制
    '''
    _obj = None# 控制句柄

    @classmethod
    def load_file(cls, dir_path: str = None, base_name: str = '全局配置') -> None:
        # 已初始化
        if cls._obj:
            cls._obj.load(False)
            return None
        # 存放文件夹
        if not dir_path:
            main_module_path = os.path.abspath(sys.argv[0])
            dir_path = os.path.dirname(main_module_path)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
        # 文件名
        if not base_name:
            base_name = '全局配置.ini'
        if not base_name.lower().endswith('.ini'):
            base_name += '.ini'
        # 文件路径
        ini_path = os.path.join(dir_path, base_name)
        # 创建配置
        cls._obj = IniConfig(ini_path)

    @classmethod
    def save_to_file(cls) -> None:
        """保存到文件
        """
        cls._obj.save()

    @classmethod
    def load(cls, section: str, key: str, default: str) -> str:
        """加载配置
        section: 节 (__name__)
        key: 键
        default: 默认
        """
        return cls._obj.get_value(section, key, default)

    @classmethod
    def save(cls, section: str, key: str, value: str) -> None:
        """保存
        section: 节 (__name__)
        key: 键
        value: 值
        """
        cls._obj.set_value(section, key, value)


# ini配置文件控制
class IniConfig(object):
    '''ini配置文件控制
    '''
    def __init__(self, ini_path: str) -> None:
        '''构造
        ini_path: ini配置文件路径
        '''
        if not ini_path.endswith('.ini'):
            raise ValueError from IniConfig
        self.__ini_path = os.path.abspath(ini_path)# ini文件路径
        self.__cfg_parser = ConfigParser()# 解析器
        self.__has_changed = False# 存在改动
        self.load()# 加载配置

    def __repr__(self) -> str:
        '''实例化对象的输出信息
        '''
        return f'ini path={self.__ini_path}'

    def get_ini_path(self) -> str:
        '''ini文件路径
        '''
        return self.__ini_path

    def load(self, force_load=False) -> bool:
        '''加载配置
        force_load: =True, 忽略内存中的改动, 强制加载配置
        '''
        if not os.path.isfile(self.__ini_path):
            self.__has_changed = True
            return False
        if not force_load and self.__has_changed:
            return False
        self.__cfg_parser.read(self.__ini_path)
        self.__has_changed = False
        return True

    def save(self) -> None:
        '''保存配置
        '''
        if self.__has_changed:
            self.__has_changed = False
            with open(self.__ini_path, 'w') as fp:
                self.__cfg_parser.write(fp)

    def __create_section(self, section: str) -> None:
        '''创建节
        '''
        if not self.__cfg_parser.has_section(section):
            self.__cfg_parser.add_section(section)

    def set_value(self, section: str, key: str, value: str) -> None:
        '''写配置
        section: 节 (可直接使用 __name__)
        key: 键
        value: 键值
        '''
        self.__has_changed = True
        self.__create_section(section)
        self.__cfg_parser.set(section, key, value)

    def __has_key(self, section: str, key: str) -> bool:
        '''键是否在节中
        '''
        return key in self.__cfg_parser.options(section)

    def get_value(self, section: str, key: str, default: str) -> str:
        '''读配置
        '''
        if not self.__cfg_parser.has_section(section) or not self.__has_key(section, key):
            return default
        return self.__cfg_parser.get(section, key)
