// 游戏状态枚举
const GameState = {
    MAIN_MENU: 'main_menu',
    NARRATIVE: 'narrative',
    COMBAT: 'combat',
    GAME_OVER: 'game_over'
};

// 游戏管理器
class GameManager {
    constructor() {
        // 当前游戏状态
        this.currentState = GameState.MAIN_MENU;
        
        // 场景元素
        this.mainMenuArea = document.getElementById('main-menu-area');
        this.narrativeArea = document.getElementById('narrative-area');
        this.combatArea = document.getElementById('combat-area');
        this.gameOverArea = document.getElementById('game-over-area');
        
        // 初始化各个管理器
        this.narrativeManager = new NarrativeManager(this);
        this.combatManager = new CombatManager(this);
        
        // 绑定按钮事件
        this.bindButtons();
    }
    
    // 初始化游戏
    init() {
        this.changeState(GameState.MAIN_MENU);
    }
    
    // 切换游戏状态
    changeState(newState) {
        this.currentState = newState;
        
        // 隐藏所有场景
        this.mainMenuArea.classList.add('hidden');
        this.narrativeArea.classList.add('hidden');
        this.combatArea.classList.add('hidden');
        this.gameOverArea.classList.add('hidden');
        
        // 显示当前场景
        switch (newState) {
            case GameState.MAIN_MENU:
                this.mainMenuArea.classList.remove('hidden');
                break;
            case GameState.NARRATIVE:
                this.narrativeArea.classList.remove('hidden');
                this.narrativeManager.startNarrative();
                break;
            case GameState.COMBAT:
                this.combatArea.classList.remove('hidden');
                this.combatManager.startCombat();
                break;
            case GameState.GAME_OVER:
                this.gameOverArea.classList.remove('hidden');
                break;
        }
    }
    
    // 绑定按钮事件
    bindButtons() {
        // 主菜单按钮
        document.getElementById('start-button').addEventListener('click', () => {
            this.changeState(GameState.NARRATIVE);
        });
        
        document.getElementById('load-button').addEventListener('click', () => {
            this.loadGame();
        });
        
        document.getElementById('quit-button').addEventListener('click', () => {
            if (confirm('确定要退出游戏吗？')) {
                window.close();
            }
        });
        
        // 游戏结束按钮
        document.getElementById('restart-button').addEventListener('click', () => {
            this.changeState(GameState.MAIN_MENU);
        });
        
        document.getElementById('quit-game-button').addEventListener('click', () => {
            if (confirm('确定要退出游戏吗？')) {
                window.close();
            }
        });
    }
    
    // 保存游戏
    saveGame() {
        const saveData = {
            narrativeState: this.narrativeManager.currentSceneId,
            player: this.combatManager.player
        };
        
        localStorage.setItem('rpgGameSave', JSON.stringify(saveData));
        alert('游戏已保存！');
    }
    
    // 加载游戏
    loadGame() {
        const saveData = localStorage.getItem('rpgGameSave');
        
        if (saveData) {
            const data = JSON.parse(saveData);
            
            // 恢复叙事状态
            this.narrativeManager.currentSceneId = data.narrativeState;
            
            // 恢复玩家状态
            this.combatManager.player = data.player;
            
            // 切换到叙事场景
            this.changeState(GameState.NARRATIVE);
            
            alert('游戏已加载！');
        } else {
            alert('没有找到存档！');
        }
    }
}

// 叙事管理器
class NarrativeManager {
    constructor(gameManager) {
        this.gameManager = gameManager;
        
        // 叙事元素
        this.backgroundElement = document.getElementById('background');
        this.characterPortraitElement = document.getElementById('character-portrait');
        this.textBoxElement = document.getElementById('text-box');
        this.choicesAreaElement = document.getElementById('choices-area');
        
        // 当前场景ID
        this.currentSceneId = 'intro';
        
        // 场景数据
        this.scenes = {
            'intro': {
                text: '这是一个测试剧情。你是一名勇敢的冒险者，正在探索一座古老的遗迹。突然，你遇到了一个神秘的生物...',
                background: 'url("images/default_background.jpg")',
                portrait: 'url("images/player.jpg")',
                choices: [
                    { text: '与生物交谈', nextScene: 'talk' },
                    { text: '准备战斗', nextScene: 'combat' }
                ]
            },
            'talk': {
                text: '你决定与神秘生物交谈。它似乎很友好，告诉你关于这座遗迹的秘密...',
                background: 'url("images/default_background.jpg")',
                portrait: 'url("images/player.jpg")',
                choices: [
                    { text: '继续探索', nextScene: 'explore' }
                ]
            },
            'explore': {
                text: '你继续探索遗迹，发现了一个古老的宝箱。当你靠近时，一个守卫者出现了！',
                background: 'url("images/default_background.jpg")',
                portrait: 'url("images/player.jpg")',
                choices: [
                    { text: '准备战斗', nextScene: 'combat' }
                ]
            }
        };
    }
    
    // 开始叙事
    startNarrative() {
        this.showScene(this.currentSceneId);
    }
    
    // 显示场景
    showScene(sceneId) {
        const scene = this.scenes[sceneId];
        
        if (!scene) {
            console.error(`场景 ${sceneId} 不存在`);
            return;
        }
        
        // 更新当前场景ID
        this.currentSceneId = sceneId;
        
        // 设置背景
        this.backgroundElement.style.backgroundImage = scene.background;
        
        // 设置角色立绘
        this.characterPortraitElement.style.backgroundImage = scene.portrait;
        
        // 设置文本
        this.textBoxElement.textContent = scene.text;
        
        // 清空选项区域
        this.choicesAreaElement.innerHTML = '';
        
        // 添加选项按钮
        scene.choices.forEach(choice => {
            const button = document.createElement('button');
            button.className = 'choice-button';
            button.textContent = choice.text;
            
            button.addEventListener('click', () => {
                if (choice.nextScene === 'combat') {
                    this.gameManager.changeState(GameState.COMBAT);
                } else {
                    this.showScene(choice.nextScene);
                }
            });
            
            this.choicesAreaElement.appendChild(button);
        });
    }
}

// 角色类
class Character {
    constructor(name, maxHp, maxMp, attack, defense, speed) {
        this.name = name;
        this.maxHp = maxHp;
        this.maxMp = maxMp;
        this.attack = attack;
        this.defense = defense;
        this.speed = speed;
        
        // 当前状态
        this.currentHp = maxHp;
        this.currentMp = maxMp;
        
        // 战斗相关
        this.attackCooldown = 0;
        this.skillCooldown = 0;
        this.gcd = 0;
    }
    
    isAlive() {
        return this.currentHp > 0;
    }
    
    takeDamage(damage) {
        // 计算实际伤害（考虑防御）
        const actualDamage = Math.max(1, damage - Math.floor(this.defense / 2));
        
        // 减少生命值
        this.currentHp = Math.max(0, this.currentHp - actualDamage);
        
        return actualDamage;
    }
    
    heal(amount) {
        // 计算实际恢复量
        const beforeHeal = this.currentHp;
        this.currentHp = Math.min(this.maxHp, this.currentHp + amount);
        const actualHeal = this.currentHp - beforeHeal;
        
        return actualHeal;
    }
    
    useMp(amount) {
        if (this.currentMp >= amount) {
            this.currentMp -= amount;
            return true;
        }
        return false;
    }
    
    getAttackInterval() {
        // 基础攻击间隔为2秒，速度越高，间隔越短
        return Math.max(0.5, 2.0 - (this.speed * 0.1));
    }
}

// 战斗管理器
class CombatManager {
    constructor(gameManager) {
        this.gameManager = gameManager;
        
        // 战斗元素
        this.playerHpBar = document.querySelector('#player-character .hp-bar-fill');
        this.playerHpText = document.querySelector('#player-character .hp-bar-text');
        this.playerMpBar = document.querySelector('#player-character .mp-bar-fill');
        this.playerMpText = document.querySelector('#player-character .mp-bar-text');
        
        this.enemyHpBar = document.querySelector('#enemy-character .hp-bar-fill');
        this.enemyHpText = document.querySelector('#enemy-character .hp-bar-text');
        
        this.allyCharacter = document.getElementById('ally-character');
        this.allyHpBar = document.querySelector('#ally-character .hp-bar-fill');
        this.allyHpText = document.querySelector('#ally-character .hp-bar-text');
        
        this.battleLog = document.getElementById('battle-log');
        
        this.skillButton = document.getElementById('skill-button');
        this.summonButton = document.getElementById('summon-button');
        
        // 创建角色
        this.player = new Character('玩家', 100, 50, 10, 5, 5);
        this.enemy = new Character('敌人', 80, 0, 8, 4, 4);
        this.ally = null;
        
        // 战斗状态
        this.battleActive = false;
        this.lastUpdateTime = 0;
        
        // 冷却时间常量
        this.SKILL_COOLDOWN = 5.0;
        this.GCD = 1.5;
        
        // 绑定按钮事件
        this.bindButtons();
    }
    
    // 开始战斗
    startCombat() {
        // 重置角色状态
        this.player.currentHp = this.player.maxHp;
        this.player.currentMp = this.player.maxMp;
        this.player.attackCooldown = 0;
        this.player.skillCooldown = 0;
        this.player.gcd = 0;
        
        this.enemy = new Character('敌人', 80, 0, 8, 4, 4);
        this.ally = null;
        this.allyCharacter.classList.add('hidden');
        
        // 清空战斗日志
        this.battleLog.innerHTML = '';
        
        // 添加初始战斗日志
        this.addBattleLog('战斗开始！');
        this.addBattleLog(`${this.player.name} vs ${this.enemy.name}`);
        
        // 更新UI
        this.updateUI();
        
        // 激活战斗
        this.battleActive = true;
        this.lastUpdateTime = Date.now();
        
        // 启动战斗循环
        this.battleLoop();
    }
    
    // 战斗循环
    battleLoop() {
        if (!this.battleActive) return;
        
        // 计算经过的时间
        const currentTime = Date.now();
        const elapsedTime = (currentTime - this.lastUpdateTime) / 1000.0;
        this.lastUpdateTime = currentTime;
        
        // 更新冷却时间
        this.updateCooldowns(this.player, elapsedTime);
        this.updateCooldowns(this.enemy, elapsedTime);
        if (this.ally) {
            this.updateCooldowns(this.ally, elapsedTime);
        }
        
        // 处理自动攻击
        if (this.player.isAlive() && this.player.attackCooldown <= 0) {
            const message = this.processAttack(this.player, this.enemy);
            this.addBattleLog(message);
        }
        
        if (this.enemy.isAlive() && this.enemy.attackCooldown <= 0) {
            const target = this.getEnemyTarget();
            if (target) {
                const message = this.processAttack(this.enemy, target);
                this.addBattleLog(message);
            }
        }
        
        if (this.ally && this.ally.isAlive() && this.ally.attackCooldown <= 0) {
            const message = this.processAttack(this.ally, this.enemy);
            this.addBattleLog(message);
        }
        
        // 更新UI
        this.updateUI();
        
        // 检查战斗是否结束
        if (this.isBattleOver()) {
            this.battleActive = false;
            
            if (this.player.currentHp <= 0) {
                this.addBattleLog('战斗失败！');
                setTimeout(() => {
                    this.gameManager.changeState(GameState.GAME_OVER);
                }, 3000);
            } else {
                this.addBattleLog('战斗胜利！获得经验值：100');
                setTimeout(() => {
                    this.gameManager.changeState(GameState.NARRATIVE);
                }, 3000);
            }
        } else {
            // 继续战斗循环
            requestAnimationFrame(() => this.battleLoop());
        }
    }
    
    // 更新冷却时间
    updateCooldowns(character, elapsedTime) {
        character.attackCooldown = Math.max(0, character.attackCooldown - elapsedTime);
        character.skillCooldown = Math.max(0, character.skillCooldown - elapsedTime);
        character.gcd = Math.max(0, character.gcd - elapsedTime);
    }
    
    // 处理攻击
    processAttack(attacker, target) {
        // 计算伤害
        const baseDamage = attacker.attack;
        const variation = 0.8 + Math.random() * 0.4;  // 伤害浮动 0.8-1.2
        const damage = Math.floor(baseDamage * variation);
        
        // 目标受到伤害
        const actualDamage = target.takeDamage(damage);
        
        // 重置攻击冷却
        attacker.attackCooldown = attacker.getAttackInterval();
        
        return `${attacker.name}攻击了${target.name}，造成${actualDamage}点伤害！`;
    }
    
    // 获取敌人的攻击目标
    getEnemyTarget() {
        // 如果有盟友，有50%几率攻击盟友
        if (this.ally && this.ally.isAlive() && Math.random() < 0.5) {
            return this.ally;
        }
        
        // 否则攻击玩家
        if (this.player.isAlive()) {
            return this.player;
        }
        
        return null;
    }
    
    // 玩家使用技能
    playerUseSkill() {
        // 检查冷却和魔法值
        if (this.player.skillCooldown > 0 || this.player.gcd > 0) {
            return 0;
        }
        
        if (!this.player.useMp(10)) {
            this.addBattleLog('魔法值不足！');
            return 0;
        }
        
        // 计算技能伤害
        const baseDamage = this.player.attack * 2;
        const variation = 0.9 + Math.random() * 0.2;  // 伤害浮动 0.9-1.1
        const damage = Math.floor(baseDamage * variation);
        
        // 敌人受到伤害
        const actualDamage = this.enemy.takeDamage(damage);
        
        // 设置冷却
        this.player.skillCooldown = this.SKILL_COOLDOWN;
        this.player.gcd = this.GCD;
        
        this.addBattleLog(`${this.player.name}使用火球术，对${this.enemy.name}造成${actualDamage}点伤害！`);
        
        return actualDamage;
    }
    
    // 玩家召唤盟友
    playerSummonAlly() {
        if (this.ally) {
            this.addBattleLog('已经召唤了盟友！');
            return;
        }
        
        if (!this.player.useMp(20)) {
            this.addBattleLog('魔法值不足！');
            return;
        }
        
        this.ally = new Character('盟友', 60, 0, 7, 3, 6);
        this.allyCharacter.classList.remove('hidden');
        
        this.addBattleLog(`${this.player.name}召唤了${this.ally.name}！`);
    }
    
    // 检查战斗是否结束
    isBattleOver() {
        // 如果玩家和所有盟友都阵亡，战斗失败
        const playerSideAlive = this.player.isAlive() || (this.ally && this.ally.isAlive());
        
        // 如果敌人阵亡，战斗胜利
        const enemySideAlive = this.enemy.isAlive();
        
        return !playerSideAlive || !enemySideAlive;
    }
    
    // 更新UI
    updateUI() {
        // 更新玩家HP/MP
        const playerHpPercent = (this.player.currentHp / this.player.maxHp) * 100;
        this.playerHpBar.style.width = `${playerHpPercent}%`;
        this.playerHpText.textContent = `${this.player.currentHp}/${this.player.maxHp}`;
        
        const playerMpPercent = (this.player.currentMp / this.player.maxMp) * 100;
        this.playerMpBar.style.width = `${playerMpPercent}%`;
        this.playerMpText.textContent = `${this.player.currentMp}/${this.player.maxMp}`;
        
        // 更新敌人HP
        const enemyHpPercent = (this.enemy.currentHp / this.enemy.maxHp) * 100;
        this.enemyHpBar.style.width = `${enemyHpPercent}%`;
        this.enemyHpText.textContent = `${this.enemy.currentHp}/${this.enemy.maxHp}`;
        
        // 更新盟友HP（如果有）
        if (this.ally) {
            const allyHpPercent = (this.ally.currentHp / this.ally.maxHp) * 100;
            this.allyHpBar.style.width = `${allyHpPercent}%`;
            this.allyHpText.textContent = `${this.ally.currentHp}/${this.ally.maxHp}`;
        }
        
        // 更新技能按钮状态
        this.skillButton.disabled = this.player.skillCooldown > 0 || this.player.gcd > 0 || this.player.currentMp < 10;
        this.summonButton.disabled = this.ally !== null || this.player.currentMp < 20;
    }
    
    // 添加战斗日志
    addBattleLog(message) {
        const logEntry = document.createElement('div');
        logEntry.className = 'log-entry';
        logEntry.textContent = message;
        
        this.battleLog.appendChild(logEntry);
        this.battleLog.scrollTop = this.battleLog.scrollHeight;
    }
    
    // 绑定按钮事件
    bindButtons() {
        this.skillButton.addEventListener('click', () => {
            if (this.battleActive) {
                this.playerUseSkill();
                this.updateUI();
            }
        });
        
        this.summonButton.addEventListener('click', () => {
            if (this.battleActive) {
                this.playerSummonAlly();
                this.updateUI();
            }
        });
    }
}

// 当DOM加载完毕后初始化游戏
document.addEventListener('DOMContentLoaded', () => {
    const gameManager = new GameManager();
    gameManager.init();
});