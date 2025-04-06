#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
HP条UI组件
用于显示角色的生命值
"""

import pygame

class HPBar:
    """HP条类"""
    
    def __init__(self, x, y, width, height, character):
        """初始化HP条
        
        Args:
            x: HP条左上角x坐标
            y: HP条左上角y坐标
            width: HP条宽度
            height: HP条高度
            character: 角色对象
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.character = character
        
        # HP条颜色
        self.bg_color = (50, 50, 50)
        self.border_color = (200, 200, 200)
        self.hp_color = (50, 200, 50)
        self.text_color = (255, 255, 255)
        
        # 创建字体
        self.font = pygame.font.SysFont("simhei", 16)
    
    def draw(self, screen):
        """绘制HP条
        
        Args:
            screen: Pygame显示表面
        """
        # 绘制背景
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=3)
        
        # 计算当前HP比例
        hp_ratio = self.character.current_hp / self.character.max_hp
        hp_width = int(self.rect.width * hp_ratio)
        
        # 绘制HP
        hp_rect = pygame.Rect(self.rect.x, self.rect.y, hp_width, self.rect.height)
        pygame.draw.rect(screen, self.hp_color, hp_rect, border_radius=3)
        
        # 绘制边框
        pygame.draw.rect(screen, self.border_color, self.rect, width=2, border_radius=3)
        
        # 绘制文本
        text = f"{self.character.name}: {self.character.current_hp}/{self.character.max_hp}"
        text_surface = self.font.render(text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
