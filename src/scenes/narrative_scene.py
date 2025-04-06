#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
叙事场景
展示游戏剧情和对话
"""

import pygame
from src.game_state import GameState
from src.scenes.base_scene import BaseScene
from src.ui.button import Button
from src.ui.text_box import TextBox

class NarrativeScene(BaseScene):
    """叙事场景类"""

    def __init__(self, scene_manager):
        """初始化叙事场景

        Args:
            scene_manager: 场景管理器实例
        """
        super().__init__(scene_manager)

        # 屏幕尺寸
        self.screen_width = self.scene_manager.screen.get_width()
        self.screen_height = self.scene_manager.screen.get_height()

        # 加载背景图
        self.background = self.scene_manager.resource_manager.get_image("default_background")

        # 创建文本框
        text_box_width = self.screen_width - 100
        text_box_height = 150
        text_box_x = 50
        text_box_y = self.screen_height - text_box_height - 50

        self.text_box = TextBox(
            text_box_x,
            text_box_y,
            text_box_width,
            text_box_height,
            "这是一个测试剧情。你是一名勇敢的冒险者，正在探索一座古老的遗迹。突然，你遇到了一个神秘的生物..."
        )

        # 创建选项按钮
        button_width = 200
        button_height = 40
        button_margin = 20

        self.option_buttons = [
            Button(
                self.screen_width // 2 - button_width - button_margin,
                text_box_y + text_box_height + 20,
                button_width,
                button_height,
                "与生物交谈",
                self._on_talk_click
            ),
            Button(
                self.screen_width // 2 + button_margin,
                text_box_y + text_box_height + 20,
                button_width,
                button_height,
                "准备战斗",
                self._on_fight_click
            )
        ]

        # 加载角色立绘
        self.character_image = self.scene_manager.resource_manager.get_image("player")
        self.character_rect = self.character_image.get_rect()
        self.character_rect.centerx = self.screen_width // 2
        self.character_rect.y = 100

    def handle_event(self, event):
        """处理事件

        Args:
            event: Pygame事件
        """
        for button in self.option_buttons:
            button.handle_event(event)

    def update(self):
        """更新场景状态"""
        pass

    def draw(self, screen):
        """绘制场景

        Args:
            screen: Pygame显示表面
        """
        # 绘制背景
        screen.blit(self.background, (0, 0))

        # 绘制角色立绘
        screen.blit(self.character_image, self.character_rect)

        # 绘制文本框
        self.text_box.draw(screen)

        # 绘制选项按钮
        for button in self.option_buttons:
            button.draw(screen)

    def _on_talk_click(self):
        """交谈选项点击事件处理"""
        # 更新文本框内容
        self.text_box.set_text("你决定与神秘生物交谈。它似乎很友好，告诉你关于这座遗迹的秘密...")

        # 更新选项按钮
        self.option_buttons = [
            Button(
                self.screen_width // 2 - 100,
                self.text_box.rect.bottom + 20,
                200,
                40,
                "继续探索",
                self._on_continue_click
            )
        ]

    def _on_fight_click(self):
        """战斗选项点击事件处理"""
        # 切换到战斗场景
        self.scene_manager.change_state(GameState.COMBAT)

    def _on_continue_click(self):
        """继续探索选项点击事件处理"""
        # 更新文本框内容
        self.text_box.set_text("你继续探索遗迹，发现了一个古老的宝箱。当你靠近时，一个守卫者出现了！")

        # 更新选项按钮
        self.option_buttons = [
            Button(
                self.screen_width // 2 - 100,
                self.text_box.rect.bottom + 20,
                200,
                40,
                "准备战斗",
                self._on_fight_click
            )
        ]
