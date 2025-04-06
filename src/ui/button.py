#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
按钮UI组件
"""

import pygame

class Button:
    """按钮类"""
    
    def __init__(self, x, y, width, height, text, on_click=None):
        """初始化按钮
        
        Args:
            x: 按钮左上角x坐标
            y: 按钮左上角y坐标
            width: 按钮宽度
            height: 按钮高度
            text: 按钮文本
            on_click: 点击事件回调函数
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.on_click = on_click
        
        # 按钮状态
        self.is_hovered = False
        
        # 按钮颜色
        self.normal_color = (100, 100, 100)
        self.hover_color = (150, 150, 150)
        self.text_color = (255, 255, 255)
        
        # 创建字体
        self.font = pygame.font.SysFont("simhei", 24)
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)
    
    def handle_event(self, event):
        """处理事件
        
        Args:
            event: Pygame事件
        """
        if event.type == pygame.MOUSEMOTION:
            # 检测鼠标悬停
            self.is_hovered = self.rect.collidepoint(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 检测鼠标点击
            if event.button == 1 and self.rect.collidepoint(event.pos):
                if self.on_click:
                    self.on_click()
    
    def draw(self, screen):
        """绘制按钮
        
        Args:
            screen: Pygame显示表面
        """
        # 绘制按钮背景
        color = self.hover_color if self.is_hovered else self.normal_color
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        
        # 绘制按钮边框
        pygame.draw.rect(screen, (200, 200, 200), self.rect, width=2, border_radius=5)
        
        # 绘制按钮文本
        screen.blit(self.text_surface, self.text_rect)
