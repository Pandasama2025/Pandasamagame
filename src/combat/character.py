#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
角色类
定义游戏中的角色属性和行为
"""

class Character:
    """角色类"""
    
    def __init__(self, name, max_hp, max_mp, attack, defense, speed):
        """初始化角色
        
        Args:
            name: 角色名称
            max_hp: 最大生命值
            max_mp: 最大魔法值
            attack: 攻击力
            defense: 防御力
            speed: 速度
        """
        self.name = name
        self.max_hp = max_hp
        self.max_mp = max_mp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        
        # 当前状态
        self.current_hp = max_hp
        self.current_mp = max_mp
        
        # 战斗相关
        self.attack_cooldown = 0  # 攻击冷却时间
        self.skill_cooldown = 0   # 技能冷却时间
        self.gcd = 0              # 公共冷却时间
    
    def is_alive(self):
        """检查角色是否存活
        
        Returns:
            bool: 是否存活
        """
        return self.current_hp > 0
    
    def take_damage(self, damage):
        """受到伤害
        
        Args:
            damage: 伤害值
            
        Returns:
            int: 实际受到的伤害
        """
        # 计算实际伤害（考虑防御）
        actual_damage = max(1, damage - self.defense // 2)
        
        # 减少生命值
        self.current_hp = max(0, self.current_hp - actual_damage)
        
        return actual_damage
    
    def heal(self, amount):
        """恢复生命值
        
        Args:
            amount: 恢复量
            
        Returns:
            int: 实际恢复的生命值
        """
        # 计算实际恢复量
        before_heal = self.current_hp
        self.current_hp = min(self.max_hp, self.current_hp + amount)
        actual_heal = self.current_hp - before_heal
        
        return actual_heal
    
    def use_mp(self, amount):
        """消耗魔法值
        
        Args:
            amount: 消耗量
            
        Returns:
            bool: 是否成功消耗
        """
        if self.current_mp >= amount:
            self.current_mp -= amount
            return True
        return False
    
    def get_attack_interval(self):
        """获取攻击间隔
        
        Returns:
            float: 攻击间隔（秒）
        """
        # 基础攻击间隔为2秒，速度越高，间隔越短
        return max(0.5, 2.0 - (self.speed * 0.1))
