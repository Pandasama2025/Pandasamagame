#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
资源管理器
负责加载和管理游戏资源
"""

import os
import pygame

class ResourceManager:
    """资源管理器类"""
    
    def __init__(self):
        """初始化资源管理器"""
        self.images = {}
        self.fonts = {}
        
        # 创建默认资源
        self._create_default_resources()
    
    def _create_default_resources(self):
        """创建默认资源"""
        # 创建默认背景图
        bg_surface = pygame.Surface((800, 600))
        bg_surface.fill((80, 60, 80))  # 紫色背景
        for i in range(0, 800, 20):
            for j in range(0, 600, 20):
                if (i + j) % 40 == 0:
                    pygame.draw.rect(bg_surface, (90, 70, 90), (i, j, 20, 20))
        self.images["default_background"] = bg_surface
        
        # 创建默认角色立绘
        player_surface = pygame.Surface((100, 150))
        player_surface.fill((100, 100, 200))
        pygame.draw.circle(player_surface, (150, 150, 250), (50, 40), 30)
        pygame.draw.rect(player_surface, (100, 100, 180), (30, 80, 40, 70))
        self.images["player"] = player_surface
        
        enemy_surface = pygame.Surface((100, 150))
        enemy_surface.fill((200, 100, 100))
        pygame.draw.circle(enemy_surface, (250, 150, 150), (50, 40), 30)
        pygame.draw.rect(enemy_surface, (180, 100, 100), (30, 80, 40, 70))
        self.images["enemy"] = enemy_surface
        
        ally_surface = pygame.Surface((80, 120))
        ally_surface.fill((100, 200, 100))
        pygame.draw.circle(ally_surface, (150, 250, 150), (40, 30), 25)
        pygame.draw.rect(ally_surface, (100, 180, 100), (25, 60, 30, 60))
        self.images["ally"] = ally_surface
    
    def get_image(self, name):
        """获取图像
        
        Args:
            name: 图像名称
            
        Returns:
            Surface: Pygame表面对象
        """
        return self.images.get(name)
    
    def get_font(self, name, size):
        """获取字体
        
        Args:
            name: 字体名称
            size: 字体大小
            
        Returns:
            Font: Pygame字体对象
        """
        key = f"{name}_{size}"
        if key not in self.fonts:
            self.fonts[key] = pygame.font.SysFont(name, size)
        return self.fonts[key]
