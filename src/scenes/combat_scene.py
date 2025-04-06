#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
战斗场景
实现基于冷却和速度的战斗系统
"""

import pygame
from src.game_state import GameState
from src.scenes.base_scene import BaseScene
from src.ui.button import Button
from src.ui.hp_bar import HPBar
from src.ui.battle_log import BattleLog
from src.combat.battle_manager import BattleManager
from src.combat.character import Character

class CombatScene(BaseScene):
    """战斗场景类"""

    def __init__(self, scene_manager):
        """初始化战斗场景

        Args:
            scene_manager: 场景管理器实例
        """
        super().__init__(scene_manager)

        # 屏幕尺寸
        self.screen_width = self.scene_manager.screen.get_width()
        self.screen_height = self.scene_manager.screen.get_height()

        # 创建角色
        self.player = Character("玩家", 100, 50, 10, 5, 5)
        self.enemy = Character("敌人", 80, 0, 8, 4, 4)
        self.ally = None  # 初始没有盟友

        # 创建战斗管理器
        self.battle_manager = BattleManager(self.player, self.enemy)

        # 创建HP条
        hp_bar_width = 200
        hp_bar_height = 20
        player_hp_bar_x = 50
        enemy_hp_bar_x = self.screen_width - 50 - hp_bar_width
        hp_bar_y = 50

        self.player_hp_bar = HPBar(
            player_hp_bar_x,
            hp_bar_y,
            hp_bar_width,
            hp_bar_height,
            self.player
        )

        self.enemy_hp_bar = HPBar(
            enemy_hp_bar_x,
            hp_bar_y,
            hp_bar_width,
            hp_bar_height,
            self.enemy
        )

        self.ally_hp_bar = None  # 初始没有盟友HP条

        # 创建战斗日志
        log_width = self.screen_width - 100
        log_height = 150
        log_x = 50
        log_y = self.screen_height - log_height - 100

        self.battle_log = BattleLog(
            log_x,
            log_y,
            log_width,
            log_height
        )

        # 添加初始战斗日志
        self.battle_log.add_message("战斗开始！")
        self.battle_log.add_message(f"{self.player.name} vs {self.enemy.name}")

        # 创建技能按钮
        button_width = 150
        button_height = 40
        button_margin = 20
        button_y = log_y + log_height + 20

        self.skill_button = Button(
            self.screen_width // 2 - button_width - button_margin,
            button_y,
            button_width,
            button_height,
            "火球术 (MP: 10)",
            self._on_skill_click
        )

        self.summon_button = Button(
            self.screen_width // 2 + button_margin,
            button_y,
            button_width,
            button_height,
            "召唤盟友 (MP: 20)",
            self._on_summon_click
        )

        # 战斗状态
        self.battle_active = True
        self.last_update_time = pygame.time.get_ticks()

    def handle_event(self, event):
        """处理事件

        Args:
            event: Pygame事件
        """
        if self.battle_active:
            self.skill_button.handle_event(event)
            self.summon_button.handle_event(event)

        # 处理用户自定义事件
        if event.type == pygame.USEREVENT:
            if hasattr(event, 'dict') and 'action' in event.dict:
                if event.dict['action'] == 'game_over':
                    self.scene_manager.change_state(GameState.GAME_OVER)
                elif event.dict['action'] == 'back_to_narrative':
                    self.scene_manager.change_state(GameState.NARRATIVE)

    def update(self):
        """更新场景状态"""
        if not self.battle_active:
            return

        # 获取当前时间
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.last_update_time) / 1000.0  # 转换为秒
        self.last_update_time = current_time

        # 更新战斗
        battle_events = self.battle_manager.update(elapsed_time)

        # 处理战斗事件
        for event in battle_events:
            self.battle_log.add_message(event)

        # 检查战斗是否结束
        if self.battle_manager.is_battle_over():
            self.battle_active = False

            if self.player.current_hp <= 0:
                self.battle_log.add_message("战斗失败！")
                # 延迟一段时间后切换到游戏结束场景
                pygame.time.set_timer(pygame.USEREVENT, 3000)
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"action": "game_over"}))
            else:
                self.battle_log.add_message("战斗胜利！获得经验值：100")
                # 延迟一段时间后切换回叙事场景
                pygame.time.set_timer(pygame.USEREVENT, 3000)
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"action": "back_to_narrative"}))

    def draw(self, screen):
        """绘制场景

        Args:
            screen: Pygame显示表面
        """
        # 绘制背景
        background = self.scene_manager.resource_manager.get_image("default_background")
        screen.blit(background, (0, 0))

        # 绘制角色
        player_image = self.scene_manager.resource_manager.get_image("player")
        enemy_image = self.scene_manager.resource_manager.get_image("enemy")

        screen.blit(player_image, (100, 100))  # 玩家
        screen.blit(enemy_image, (600, 100))  # 敌人

        if self.ally:
            ally_image = self.scene_manager.resource_manager.get_image("ally")
            screen.blit(ally_image, (250, 150))  # 盟友

        # 绘制HP条
        self.player_hp_bar.draw(screen)
        self.enemy_hp_bar.draw(screen)

        if self.ally_hp_bar:
            self.ally_hp_bar.draw(screen)

        # 绘制战斗日志
        self.battle_log.draw(screen)

        # 绘制技能按钮
        self.skill_button.draw(screen)
        self.summon_button.draw(screen)

    def _on_skill_click(self):
        """技能按钮点击事件处理"""
        if self.player.current_mp >= 10:
            damage = self.battle_manager.player_use_skill()
            self.battle_log.add_message(f"{self.player.name}使用火球术，对{self.enemy.name}造成{damage}点伤害！")
        else:
            self.battle_log.add_message("魔法值不足！")

    def _on_summon_click(self):
        """召唤按钮点击事件处理"""
        if self.ally:
            self.battle_log.add_message("已经召唤了盟友！")
            return

        if self.player.current_mp >= 20:
            self.ally = Character("盟友", 60, 0, 7, 3, 6)
            self.battle_manager.add_ally(self.ally)
            self.player.current_mp -= 20

            # 创建盟友HP条
            ally_hp_bar_x = self.screen_width // 2 - 100
            ally_hp_bar_y = 80
            self.ally_hp_bar = HPBar(
                ally_hp_bar_x,
                ally_hp_bar_y,
                200,
                20,
                self.ally
            )

            self.battle_log.add_message(f"{self.player.name}召唤了{self.ally.name}！")
        else:
            self.battle_log.add_message("魔法值不足！")
