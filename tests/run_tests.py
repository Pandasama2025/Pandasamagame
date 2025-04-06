#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试运行器
运行所有单元测试
"""

import unittest
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

if __name__ == '__main__':
    # 自动发现并运行所有测试
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(os.path.dirname(__file__), pattern='test_*.py')
    
    # 运行测试
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # 根据测试结果设置退出码
    sys.exit(not result.wasSuccessful())