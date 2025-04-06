#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
奇幻小说TRPG游戏原型
主程序入口
"""

import pygame
import sys
from src.game_state import GameState
from src.scene_manager import SceneManager

# 初始化Pygame
pygame.init()

# 游戏窗口设置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("奇幻小说TRPG游戏原型")

# 初始化场景管理器
scene_manager = SceneManager(screen)

# 游戏主循环
clock = pygame.time.Clock()
running = True

while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        scene_manager.handle_event(event)
    
    # 更新游戏状态
    scene_manager.update()
    
    # 绘制画面
    screen.fill((0, 0, 0))  # 清空屏幕，使用黑色背景
    scene_manager.draw()
    pygame.display.flip()  # 更新屏幕显示
    
    # 控制帧率
    clock.tick(60)

# 退出游戏
pygame.quit()
sys.exit()
