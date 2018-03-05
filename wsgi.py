#!/usr/bin/env python3

import sys
from os.path import abspath
from os.path import dirname
import app

# 当前运行脚本的绝对路径插入到 python 搜索模块的路径集（list） 第一个位置
sys.path.insert(0, abspath(dirname(__file__)))
application = app.configured_app()


