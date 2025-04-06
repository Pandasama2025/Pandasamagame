#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
战斗管理器
管理战斗流程和逻辑
"""

import random

class BattleManager:
    """战斗管理器类"""
    
    def __init__(self, player, enemy):
        """初始化战斗管理器
        
        Args:
            player: 玩家角色
            enemy: 敌人角色
        """
        self.player = player
        self.enemy = enemy
        self.allies = []  # 盟友列表
        
        # 战斗状态
        self.battle_active = True
        
        # 冷却时间常量
        self.SKILL_COOLDOWN = 5.0  # 技能冷却时间（秒）
        self.GCD = 1.5             # 公共冷却时间（秒）
    
    def update(self, elapsed_time):
        """更新战斗状态
        
        Args:
            elapsed_time: 经过的时间（秒）
            
        Returns:
            list: 战斗事件消息列表
        """
        if not self.battle_active:
            return []
        
        events = []
        
        # 更新玩家冷却时间
        self._update_cooldowns(self.player, elapsed_time)
        
        # 更新敌人冷却时间
        self._update_cooldowns(self.enemy, elapsed_time)
        
        # 更新盟友冷却时间
        for ally in self.allies:
            self._update_cooldowns(ally, elapsed_time)
        
        # 处理自动攻击
        if self.player.is_alive() and self.player.attack_cooldown <= 0:
            events.append(self._process_attack(self.player, self.enemy))
        
        if self.enemy.is_alive() and self.enemy.attack_cooldown <= 0:
            target = self._get_enemy_target()
            if target:
                events.append(self._process_attack(self.enemy, target))
        
        for ally in self.allies:
            if ally.is_alive() and ally.attack_cooldown <= 0:
                events.append(self._process_attack(ally, self.enemy))
        
        # 检查战斗是否结束
        if self.is_battle_over():
            self.battle_active = False
        
        return events
    
    def _update_cooldowns(self, character, elapsed_time):
        """更新角色的冷却时间
        
        Args:
            character: 角色对象
            elapsed_time: 经过的时间（秒）
        """
        character.attack_cooldown = max(0, character.attack_cooldown - elapsed_time)
        character.skill_cooldown = max(0, character.skill_cooldown - elapsed_time)
        character.gcd = max(0, character.gcd - elapsed_time)
    
    def _process_attack(self, attacker, target):
        """处理攻击
        
        Args:
            attacker: 攻击者
            target: 目标
            
        Returns:
            str: 攻击事件消息
        """
        # 计算伤害
        base_damage = attacker.attack
        variation = random.uniform(0.8, 1.2)  # 伤害浮动
        damage = int(base_damage * variation)
        
        # 目标受到伤害
        actual_damage = target.take_damage(damage)
        
        # 重置攻击冷却
        attacker.attack_cooldown = attacker.get_attack_interval()
        
        return f"{attacker.name}攻击了{target.name}，造成{actual_damage}点伤害！"
    
    def _get_enemy_target(self):
        """获取敌人的攻击目标
        
        Returns:
            Character: 目标角色
        """
        # 如果有盟友，有50%几率攻击盟友
        if self.allies and random.random() < 0.5:
            # 选择一个存活的盟友
            alive_allies = [ally for ally in self.allies if ally.is_alive()]
            if alive_allies:
                return random.choice(alive_allies)
        
        # 否则攻击玩家
        if self.player.is_alive():
            return self.player
        
        return None
    
    def player_use_skill(self):
        """玩家使用技能
        
        Returns:
            int: 造成的伤害
        """
        # 检查冷却和魔法值
        if self.player.skill_cooldown > 0 or self.player.gcd > 0:
            return 0
        
        if not self.player.use_mp(10):
            return 0
        
        # 计算技能伤害
        base_damage = self.player.attack * 2
        variation = random.uniform(0.9, 1.1)
        damage = int(base_damage * variation)
        
        # 敌人受到伤害
        actual_damage = self.enemy.take_damage(damage)
        
        # 设置冷却
        self.player.skill_cooldown = self.SKILL_COOLDOWN
        self.player.gcd = self.GCD
        
        return actual_damage
    
    def add_ally(self, ally):
        """添加盟友
        
        Args:
            ally: 盟友角色
        """
        self.allies.append(ally)
    
    def is_battle_over(self):
        """检查战斗是否结束
        
        Returns:
            bool: 战斗是否结束
        """
        # 如果玩家和所有盟友都阵亡，战斗失败
        player_side_alive = self.player.is_alive() or any(ally.is_alive() for ally in self.allies)
        
        # 如果敌人阵亡，战斗胜利
        enemy_side_alive = self.enemy.is_alive()
        
        return not player_side_alive or not enemy_side_alive
