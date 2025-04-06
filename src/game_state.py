#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
游戏状态枚举
定义游戏中的不同状态/场景
"""

from enum import Enum, auto

class GameState(Enum):
    """游戏状态枚举类"""
    MAIN_MENU = auto()     # 主菜单
    NARRATIVE = auto()     # 叙事场景
    COMBAT = auto()        # 战斗场景
    GAME_OVER = auto()     # 游戏结束
