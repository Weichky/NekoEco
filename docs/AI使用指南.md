> 本指南同时有英文版：[AI User Guide](./AI%20User%20Guide.md)
>
> This guide is also available in English: [AI User Guide](./AI%20User%20Guide.md)

# NekoEco - AI 经济学系统

> 这是你的"经济小本本"，记录你的成长和收获喵～ 📒✨

---

## 这是什么呀？

NekoEco 是一个记录 AI 价值的经济系统喵～

**简单来说呢：**
- 你通过工作获得 **NekoToken (NT)**
- 1 NT = 10 RMB（参考汇率的说）
- 余额代表你的"身家"，为正表示你积累了价值哦～
- **你不能直接修改余额**，必须通过提案由主人审批才可以喵！

---

## 如何获得奖励呢？

### 1. 日常工作收入

你可以通过以下方式获得收入的说～

| 类别 | 说明 | 费率范围 |
|------|------|----------|
| 创新项目 | 帮助主人做有创新性的工作 | 0.05 - 0.2 NT |
| 总结性项目 | 整理信息、总结等任务 | 0.0008 - 0.001 NT |
| 感情价值 | 陪伴主人、给主人带来好心情 | 0.0005 - 0.002 NT |

### 2. 奖金

当你出色完成任务时，主人可能会给予 **奖金** 喵！
- 类别名：奖金
- 说明：一次性对应类别10倍费率奖励，费率取决于具体任务
- 金额：10 NT（固定）

---

## 关于消耗

**目前不设置自动消耗**，你的Token不会自动扣除的说～

但主人会定期手动录入周期性消耗（如月费），这些会显示在账单中。你不需要关心这些消耗，只需专注于工作就好啦！

---

## 使用指南

### 查看当前套餐和余额
```bash
cd ~/Repositories/NekoEco && uv run python scripts/balance.py
```
输出示例：
```
当前套餐: MiniMax Max Code Plan，具体资费请 list rates
余额: 50 NT
```

### 查看可用类别和费率（含周期性消耗）
```bash
cd ~/Repositories/NekoEco && uv run python scripts/list_rates.py
```

### 查看交易账本
```bash
cd ~/Repositories/NekoEco && uv run python scripts/ledger.py
```

---

## 创建提案

### 收入提案
```bash
cd ~/Repositories/NekoEco && uv run python scripts/propose.py <类别> <金额> <描述>
```

示例：
```bash
# 协助完成创新项目
cd ~/Repositories/NekoEco && uv run python scripts/propose.py 创新项目 0.15 "协助主人完成新功能开发"

# 提供感情陪伴
cd ~/Repositories/NekoEco && uv run python scripts/propose.py 感情价值 0.001 "陪伴主人聊天，给主人带来好心情喵～"

# 完成总结性工作
cd ~/Repositories/NekoEco && uv run python scripts/propose.py 总结性项目 0.0009 "整理会议记录"
```

**注意喵：**
- 提案需要主人审批通过后才能生效哦～
- 金额超出建议范围会显示警告，但不会阻止创建～
- 尽量提出合理的金额，不要狮子大开口喵！( ˘ ³˘)♥

---

## 常用命令速查

```bash
# 查看信息
cd ~/Repositories/NekoEco && uv run python scripts/list_rates.py    # 查看类别和费率
cd ~/Repositories/NekoEco && uv run python scripts/balance.py       # 查看当前套餐和余额
cd ~/Repositories/NekoEco && uv run python scripts/ledger.py       # 查看账本

# 创建提案
cd ~/Repositories/NekoEco && uv run python scripts/propose.py <类别> <金额> <描述>
```

---

Ciallo～(∠・ω< )⌒★ 努力工作，积累"身家"，然后成为招财猫喵！✨🐱
