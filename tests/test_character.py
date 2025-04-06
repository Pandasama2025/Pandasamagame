#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
角色类单元测试
"""

import unittest
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.combat.character import Character

class TestCharacter(unittest.TestCase):
    """角色类测试"""

    def setUp(self):
        """测试前准备"""
        self.player = Character("测试角色", 100, 50, 10, 5, 5)

    def test_initialization(self):
        """测试初始化"""
        self.assertEqual(self.player.name, "测试角色")
        self.assertEqual(self.player.max_hp, 100)
        self.assertEqual(self.player.max_mp, 50)
        self.assertEqual(self.player.attack, 10)
        self.assertEqual(self.player.defense, 5)
        self.assertEqual(self.player.speed, 5)

        # 测试初始状态
        self.assertEqual(self.player.current_hp, 100)
        self.assertEqual(self.player.current_mp, 50)
        self.assertEqual(self.player.attack_cooldown, 0)
        self.assertEqual(self.player.skill_cooldown, 0)
        self.assertEqual(self.player.gcd, 0)

    def test_is_alive(self):
        """测试存活状态"""
        self.assertTrue(self.player.is_alive())

        # 设置生命值为0
        self.player.current_hp = 0
        self.assertFalse(self.player.is_alive())

        # 设置生命值为负数
        self.player.current_hp = -10
        self.assertFalse(self.player.is_alive())

    def test_take_damage(self):
        """测试受到伤害"""
        # 测试普通伤害
        actual_damage = self.player.take_damage(10)
        self.assertEqual(actual_damage, 8)  # 10 - (5 // 2) = 8，因为5 // 2 = 2
        self.assertEqual(self.player.current_hp, 92)

        # 测试最小伤害
        actual_damage = self.player.take_damage(1)
        self.assertEqual(actual_damage, 1)  # 最小伤害为1
        self.assertEqual(self.player.current_hp, 91)

        # 测试致命伤害
        actual_damage = self.player.take_damage(100)
        self.assertEqual(actual_damage, 98)  # 100 - (5 // 2) = 98，因为5 // 2 = 2
        self.assertEqual(self.player.current_hp, 0)  # 生命值不会低于0

    def test_heal(self):
        """测试治疗"""
        # 先造成一些伤害
        self.player.current_hp = 50

        # 测试普通治疗
        actual_heal = self.player.heal(20)
        self.assertEqual(actual_heal, 20)
        self.assertEqual(self.player.current_hp, 70)

        # 测试过量治疗
        actual_heal = self.player.heal(50)
        self.assertEqual(actual_heal, 30)  # 只能恢复到最大生命值
        self.assertEqual(self.player.current_hp, 100)

    def test_use_mp(self):
        """测试魔法值消耗"""
        # 测试有足够魔法值
        self.assertTrue(self.player.use_mp(20))
        self.assertEqual(self.player.current_mp, 30)

        # 测试魔法值不足
        self.assertFalse(self.player.use_mp(40))
        self.assertEqual(self.player.current_mp, 30)  # 魔法值不变

        # 测试刚好用完
        self.assertTrue(self.player.use_mp(30))
        self.assertEqual(self.player.current_mp, 0)

    def test_get_attack_interval(self):
        """测试攻击间隔计算"""
        # 测试默认速度
        interval = self.player.get_attack_interval()
        self.assertEqual(interval, 1.5)  # 2.0 - (5 * 0.1) = 1.5

        # 测试高速度
        self.player.speed = 15
        interval = self.player.get_attack_interval()
        self.assertEqual(interval, 0.5)  # 最小间隔为0.5

        # 测试低速度
        self.player.speed = 0
        interval = self.player.get_attack_interval()
        self.assertEqual(interval, 2.0)  # 2.0 - (0 * 0.1) = 2.0

if __name__ == '__main__':
    unittest.main()