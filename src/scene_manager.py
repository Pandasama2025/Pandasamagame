#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
场景管理器
负责管理和切换不同的游戏场景
"""

import pygame
from src.game_state import GameState
from src.scenes.main_menu_scene import MainMenuScene
from src.scenes.narrative_scene import NarrativeScene
from src.scenes.combat_scene import CombatScene
from src.scenes.game_over_scene import GameOverScene

class SceneManager:
    """场景管理器类"""
    
    def __init__(self, screen):
        """初始化场景管理器
        
        Args:
            screen: Pygame显示表面
        """
        self.screen = screen
        self.current_state = GameState.MAIN_MENU
        
        # 初始化各个场景
        self.scenes = {
            GameState.MAIN_MENU: MainMenuScene(self),
            GameState.NARRATIVE: NarrativeScene(self),
            GameState.COMBAT: CombatScene(self),
            GameState.GAME_OVER: GameOverScene(self)
        }
    
    def change_state(self, new_state):
        """切换游戏状态
        
        Args:
            new_state: 新的游戏状态
        """
        self.current_state = new_state
    
    def handle_event(self, event):
        """处理事件
        
        Args:
            event: Pygame事件
        """
        self.scenes[self.current_state].handle_event(event)
    
    def update(self):
        """更新当前场景"""
        self.scenes[self.current_state].update()
    
    def draw(self):
        """绘制当前场景"""
        self.scenes[self.current_state].draw(self.screen)
