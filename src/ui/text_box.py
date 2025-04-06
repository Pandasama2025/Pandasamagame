#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
文本框UI组件
用于显示对话和叙事文本
"""

import pygame

class TextBox:
    """文本框类"""
    
    def __init__(self, x, y, width, height, text=""):
        """初始化文本框
        
        Args:
            x: 文本框左上角x坐标
            y: 文本框左上角y坐标
            width: 文本框宽度
            height: 文本框高度
            text: 文本内容
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        
        # 文本框颜色
        self.bg_color = (50, 50, 50, 200)  # 半透明背景
        self.border_color = (200, 200, 200)
        self.text_color = (255, 255, 255)
        
        # 创建字体
        self.font = pygame.font.SysFont("simhei", 24)
        
        # 文本渲染
        self.rendered_text = []
        self._render_text()
    
    def set_text(self, text):
        """设置文本内容
        
        Args:
            text: 新的文本内容
        """
        self.text = text
        self._render_text()
    
    def _render_text(self):
        """渲染文本"""
        self.rendered_text = []
        
        # 计算每行最大字符数
        max_chars_per_line = self.rect.width // (self.font.size("A")[0]) - 2
        
        # 分割文本为多行
        words = self.text.split()
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            if len(test_line) > max_chars_per_line:
                self.rendered_text.append(self.font.render(current_line, True, self.text_color))
                current_line = word + " "
            else:
                current_line = test_line
        
        if current_line:
            self.rendered_text.append(self.font.render(current_line, True, self.text_color))
    
    def draw(self, screen):
        """绘制文本框
        
        Args:
            screen: Pygame显示表面
        """
        # 创建半透明表面
        surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(surface, self.bg_color, surface.get_rect(), border_radius=10)
        screen.blit(surface, self.rect)
        
        # 绘制边框
        pygame.draw.rect(screen, self.border_color, self.rect, width=2, border_radius=10)
        
        # 绘制文本
        for i, line in enumerate(self.rendered_text):
            screen.blit(line, (self.rect.x + 10, self.rect.y + 10 + i * 30))
