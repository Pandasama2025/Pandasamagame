#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
主菜单场景
游戏的起始界面
"""

import pygame
from src.game_state import GameState
from src.scenes.base_scene import BaseScene
from src.ui.button import Button

class MainMenuScene(BaseScene):
    """主菜单场景类"""

    def __init__(self, scene_manager):
        """初始化主菜单场景

        Args:
            scene_manager: 场景管理器实例
        """
        super().__init__(scene_manager)

        # 创建按钮
        screen_width = self.scene_manager.screen.get_width()
        screen_height = self.scene_manager.screen.get_height()

        button_width = 200
        button_height = 50
        button_x = (screen_width - button_width) // 2
        button_y = screen_height // 2

        self.start_button = Button(
            button_x,
            button_y,
            button_width,
            button_height,
            "开始游戏",
            self._on_start_click
        )

        self.quit_button = Button(
            button_x,
            button_y + button_height + 20,
            button_width,
            button_height,
            "退出游戏",
            self._on_quit_click
        )

        # 设置标题
        self.title_font = pygame.font.SysFont("simhei", 48)
        self.title_text = self.title_font.render("奇幻小说TRPG游戏原型", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(screen_width // 2, screen_height // 4))

    def handle_event(self, event):
        """处理事件

        Args:
            event: Pygame事件
        """
        self.start_button.handle_event(event)
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
        background = self.scene_manager.resource_manager.get_image("default_background")
        screen.blit(background, (0, 0))

        # 绘制标题
        screen.blit(self.title_text, self.title_rect)

        # 绘制按钮
        self.start_button.draw(screen)
        self.quit_button.draw(screen)

    def _on_start_click(self):
        """开始游戏按钮点击事件处理"""
        self.scene_manager.change_state(GameState.NARRATIVE)

    def _on_quit_click(self):
        """退出游戏按钮点击事件处理"""
        pygame.quit()
        import sys
        sys.exit()
