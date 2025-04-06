#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
战斗管理器单元测试
"""

import unittest
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.combat.character import Character
from src.combat.battle_manager import BattleManager

class TestBattleManager(unittest.TestCase):
    """战斗管理器测试"""
    
    def setUp(self):
        """测试前准备"""
        self.player = Character("玩家", 100, 50, 10, 5, 5)
        self.enemy = Character("敌人", 80, 0, 8, 4, 4)
        self.battle_manager = BattleManager(self.player, self.enemy)
    
    def test_initialization(self):
        """测试初始化"""
        self.assertEqual(self.battle_manager.player, self.player)
        self.assertEqual(self.battle_manager.enemy, self.enemy)
        self.assertEqual(len(self.battle_manager.allies), 0)
        self.assertTrue(self.battle_manager.battle_active)
    
    def test_update_cooldowns(self):
        """测试冷却时间更新"""
        # 设置初始冷却时间
        self.player.attack_cooldown = 2.0
        self.player.skill_cooldown = 5.0
        self.player.gcd = 1.5
        
        # 更新冷却时间
        self.battle_manager._update_cooldowns(self.player, 1.0)
        
        # 检查冷却时间是否正确减少
        self.assertEqual(self.player.attack_cooldown, 1.0)
        self.assertEqual(self.player.skill_cooldown, 4.0)
        self.assertEqual(self.player.gcd, 0.5)
        
        # 再次更新，使部分冷却时间归零
        self.battle_manager._update_cooldowns(self.player, 1.0)
        
        # 检查冷却时间是否正确归零
        self.assertEqual(self.player.attack_cooldown, 0.0)
        self.assertEqual(self.player.skill_cooldown, 3.0)
        self.assertEqual(self.player.gcd, 0.0)
    
    def test_process_attack(self):
        """测试攻击处理"""
        # 模拟随机数，使伤害固定
        import random
        random.seed(42)
        
        # 处理攻击
        message = self.battle_manager._process_attack(self.player, self.enemy)
        
        # 检查敌人生命值是否减少
        self.assertLess(self.enemy.current_hp, 80)
        
        # 检查攻击消息是否正确
        self.assertIn("玩家攻击了敌人", message)
        self.assertIn("造成", message)
        self.assertIn("点伤害", message)
        
        # 检查攻击冷却是否重置
        self.assertGreater(self.player.attack_cooldown, 0)
    
    def test_player_use_skill(self):
        """测试玩家使用技能"""
        # 确保玩家有足够的魔法值
        self.player.current_mp = 50
        
        # 使用技能
        damage = self.battle_manager.player_use_skill()
        
        # 检查敌人生命值是否减少
        self.assertLess(self.enemy.current_hp, 80)
        
        # 检查魔法值是否减少
        self.assertEqual(self.player.current_mp, 40)
        
        # 检查技能冷却和GCD是否设置
        self.assertEqual(self.player.skill_cooldown, self.battle_manager.SKILL_COOLDOWN)
        self.assertEqual(self.player.gcd, self.battle_manager.GCD)
        
        # 尝试在冷却中使用技能
        damage = self.battle_manager.player_use_skill()
        self.assertEqual(damage, 0)  # 应该返回0，表示技能未释放
    
    def test_add_ally(self):
        """测试添加盟友"""
        # 创建盟友
        ally = Character("盟友", 60, 0, 7, 3, 6)
        
        # 添加盟友
        self.battle_manager.add_ally(ally)
        
        # 检查盟友是否添加成功
        self.assertEqual(len(self.battle_manager.allies), 1)
        self.assertEqual(self.battle_manager.allies[0], ally)
    
    def test_is_battle_over(self):
        """测试战斗结束判断"""
        # 初始状态，战斗应该继续
        self.assertFalse(self.battle_manager.is_battle_over())
        
        # 敌人阵亡，战斗应该结束
        self.enemy.current_hp = 0
        self.assertTrue(self.battle_manager.is_battle_over())
        
        # 重置敌人生命值
        self.enemy.current_hp = 80
        
        # 玩家阵亡，战斗应该结束
        self.player.current_hp = 0
        self.assertTrue(self.battle_manager.is_battle_over())
        
        # 添加盟友，玩家阵亡但盟友存活，战斗应该继续
        ally = Character("盟友", 60, 0, 7, 3, 6)
        self.battle_manager.add_ally(ally)
        self.assertFalse(self.battle_manager.is_battle_over())
        
        # 盟友也阵亡，战斗应该结束
        ally.current_hp = 0
        self.assertTrue(self.battle_manager.is_battle_over())

if __name__ == '__main__':
    unittest.main()