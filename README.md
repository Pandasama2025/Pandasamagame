# 奇幻小说TRPG游戏原型 (Python+Pygame)

这是一个使用Python和Pygame开发的奇幻小说TRPG游戏原型。该原型旨在验证核心游戏机制的可行性，包括：结合文字和少量图形元素的叙事呈现、基于选择的互动、基于冷却和速度的战斗核心循环（含召唤）、以及基础的角色扮演元素。

这是一个垂直切片原型（Vertical Slice Prototype），仅包含核心功能，用于验证技术可行性和核心玩法。

## 项目结构

```text
.
├── assets/             # 资源文件
│   ├── fonts/          # 字体资源
│   └── images/         # 图像资源
├── src/                # 源代码
│   ├── combat/         # 战斗系统
│   │   ├── battle_manager.py  # 战斗管理器
│   │   └── character.py       # 角色类
│   ├── scenes/         # 游戏场景
│   │   ├── base_scene.py      # 基础场景类
│   │   ├── combat_scene.py    # 战斗场景
│   │   ├── narrative_scene.py  # 叙事场景
│   │   └── game_over_scene.py  # 游戏结束场景
│   ├── ui/             # 用户界面组件
│   │   ├── button.py          # 按钮组件
│   │   ├── hp_bar.py          # 生命值条组件
│   │   ├── text_box.py        # 文本框组件
│   │   └── battle_log.py      # 战斗日志组件
│   ├── game_state.py    # 游戏状态枚举
│   ├── resource_manager.py  # 资源管理器
│   └── scene_manager.py    # 场景管理器
├── tests/              # 测试代码
│   ├── test_character.py   # 角色类测试
│   ├── test_battle_manager.py  # 战斗管理器测试
│   └── run_tests.py        # 测试运行器
├── main.py             # 主程序入口
├── prd.md              # 产品需求文档
├── todo.md             # 开发待办事项清单
├── README.md           # 项目说明
└── requirements.txt    # 依赖项
```

## 安装与运行

1. 确保已安装Python 3.x
2. 安装依赖项：`pip install -r requirements.txt`
3. 运行游戏：`python main.py`

## 测试

项目包含单元测试，可以通过以下方式运行：

```bash
python tests/run_tests.py
```

测试包括：

- 角色类测试：测试角色属性、伤害计算、治疗、魔法值消耗等功能
- 战斗管理器测试：测试战斗逻辑、冷却时间、技能释放、召唤等功能

## 游戏特性

- **基于场景的游戏流程**：包括主菜单、叙事场景、战斗场景和游戏结束场景
- **文本叙事与对话选择**：通过文本框展示剧情，并提供选项按钮进行互动
- **基于冷却和速度的半自动战斗系统**：角色根据速度自动攻击，玩家可以手动释放技能
- **技能和召唤系统**：玩家可以使用技能造成更高伤害，或者召唤盟友加入战斗
- **简单的角色属性系统**：包括生命值、魔法值、攻击力、防御力和速度

## 战斗系统说明

- **自动攻击**：所有角色根据自身速度自动攻击，速度越高，攻击间隔越短
- **伤害计算**：伤害基于攻击力和防御力计算，并有随机浮动
- **技能释放**：消耗魔法值，造成更高伤害，有冷却时间
- **召唤系统**：消耗魔法值，在战斗中添加一个盟友单位
- **战斗日志**：记录所有战斗事件，如攻击、伤害、技能释放等

## 控制方式

- **鼠标交互**：点击按钮进行选择和操作
- **战斗操作**：
  - 点击“火球术”按钮释放技能（消耗10点魔法值）
  - 点击“召唤盟友”按钮召唤盟友（消耗20点魔法值）

## 开发者

- Pandasama2025

## 项目状态

该项目是一个原型，已实现了基本功能。后续可能的改进方向包括：

- 添加更多的游戏内容（剧情、角色、技能等）
- 改进用户界面和视觉效果
- 添加音效和背景音乐
- 实现角色成长和升级系统
- 添加物品和装备系统
