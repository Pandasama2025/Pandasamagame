#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
游戏结束场景
显示游戏结束信息
"""

import pygame
from src.game_state import GameState
from src.scenes.base_scene import BaseScene
from src.ui.button import Button

class GameOverScene(BaseScene):
    """游戏结束场景类"""
    
    def __init__(self, scene_manager):
        """初始化游戏结束场景
        
        Args:
            scene_manager: 场景管理器实例
        """
        super().__init__(scene_manager)
        
        # 屏幕尺寸
        self.screen_width = self.scene_manager.screen.get_width()
        self.screen_height = self.scene_manager.screen.get_height()
        
        # 设置标题
        self.title_font = pygame.font.SysFont("simhei", 48)
        self.title_text = self.title_font.render("游戏结束", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 3))
        
        # 创建按钮
        button_width = 200
        button_height = 50
        button_x = (self.screen_width - button_width) // 2
        button_y = self.screen_height // 2 + 50
        
        self.restart_button = Button(
            button_x, 
            button_y, 
            button_width, 
            button_height, 
            "重新开始", 
            self._on_restart_click
        )
        
        self.quit_button = Button(
            button_x, 
            button_y + button_height + 20, 
            button_width, 
            button_height, 
            "退出游戏", 
            self._on_quit_click
        )
    
    def handle_event(self, event):
        """处理事件
        
        Args:
            event: Pygame事件
        """
        self.restart_button.handle_event(event)
        self.quit_button.handle_event(event)
    
    def update(self):
        """更新场景状态"""
        pass
    
    def draw(self, screen):
        """绘制场景
        
        Args:
            screen: Pygame显示表面
        """
        # 绘制背景
        screen.fill((40, 40, 40))  # 深灰色背景
        
        # 绘制标题
        screen.blit(self.title_text, self.title_rect)
        
        # 绘制按钮
        self.restart_button.draw(screen)
        self.quit_button.draw(screen)
    
    def _on_restart_click(self):
        """重新开始按钮点击事件处理"""
        self.scene_manager.change_state(GameState.MAIN_MENU)
    
    def _on_quit_click(self):
        """退出游戏按钮点击事件处理"""
        pygame.quit()
        import sys
        sys.exit()
