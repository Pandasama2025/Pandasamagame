#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
场景基类
所有具体场景类的父类
"""

class BaseScene:
    """场景基类"""
    
    def __init__(self, scene_manager):
        """初始化场景
        
        Args:
            scene_manager: 场景管理器实例
        """
        self.scene_manager = scene_manager
    
    def handle_event(self, event):
        """处理事件
        
        Args:
            event: Pygame事件
        """
        pass
    
    def update(self):
        """更新场景状态"""
        pass
    
    def draw(self, screen):
        """绘制场景
        
        Args:
            screen: Pygame显示表面
        """
        pass
