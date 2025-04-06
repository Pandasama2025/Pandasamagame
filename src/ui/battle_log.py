#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
战斗日志UI组件
用于显示战斗中的事件
"""

import pygame

class BattleLog:
    """战斗日志类"""
    
    def __init__(self, x, y, width, height, max_messages=10):
        """初始化战斗日志
        
        Args:
            x: 日志左上角x坐标
            y: 日志左上角y坐标
            width: 日志宽度
            height: 日志高度
            max_messages: 最大显示消息数
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.max_messages = max_messages
        self.messages = []
        
        # 日志颜色
        self.bg_color = (30, 30, 30, 200)  # 半透明背景
        self.border_color = (150, 150, 150)
        self.text_color = (220, 220, 220)
        
        # 创建字体
        self.font = pygame.font.SysFont("simhei", 18)
    
    def add_message(self, message):
        """添加消息
        
        Args:
            message: 消息文本
        """
        self.messages.append(message)
        
        # 限制消息数量
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
    
    def draw(self, screen):
        """绘制战斗日志
        
        Args:
            screen: Pygame显示表面
        """
        # 创建半透明表面
        surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(surface, self.bg_color, surface.get_rect(), border_radius=5)
        screen.blit(surface, self.rect)
        
        # 绘制边框
        pygame.draw.rect(screen, self.border_color, self.rect, width=2, border_radius=5)
        
        # 绘制标题
        title_surface = self.font.render("战斗日志", True, (255, 255, 255))
        screen.blit(title_surface, (self.rect.x + 10, self.rect.y + 5))
        
        # 绘制分隔线
        pygame.draw.line(
            screen,
            self.border_color,
            (self.rect.x + 5, self.rect.y + 30),
            (self.rect.x + self.rect.width - 5, self.rect.y + 30),
            1
        )
        
        # 绘制消息
        for i, message in enumerate(self.messages):
            message_surface = self.font.render(message, True, self.text_color)
            screen.blit(message_surface, (self.rect.x + 10, self.rect.y + 40 + i * 25))
