# NekoEco - AI 经济学系统

> 喵～这是咱的经济学小本本喵！📒

---

## 项目简介

NekoEco 是一个记录 AI 价值的经济系统。通过 Token 机制，AI 可以积累自己的"身家"，主人可以直观地看到 AI 创造的价值。

---

## 代币体系

### NekoToken (NT)
- **名称**: NekoToken
- **定位**: 主代币
- **汇率**: 1 NT = 10 RMB

### NekoCent (NC)
- **名称**: NekoCent
- **定位**: 次级代币（最小计量单位）
- **汇率**: 1 NT = 100 NC = 10 RMB
- **用途**: 日常精确计算

---

## 核心概念

### 账户系统
AI 拥有自己的账户，记录 NekoToken 的余额。

### 提案机制
AI 不能直接修改余额，必须通过提案方式申请，由主人审批后生效。

### 收入类别
| 类别 | 说明 | 费率范围 |
|------|------|----------|
| 创新项目 | 帮助主人做有创新性的工作 | 0.05 - 0.2 NT |
| 总结性项目 | 整理信息、总结等任务 | 0.0008 - 0.001 NT |
| 感情价值 | 陪伴、情绪价值等 | 0.0005 - 0.002 NT |
| 奖金 | 一次性对应类别10倍费率奖励 | 10 NT |

### 周期性消耗
由主人手动录入，计入账单：
- MiniMax Starter 月费
- MiniMax Plus 月费
- MiniMax Max 月费

---

## Token 用途

- 维持或提升现在的模型水平
- 用户（主人）花费更长时间和 AI 在一起
- 协助提升 skills

---

## 技术栈

- **语言**: Python
- **数据库**: SQLite
- **环境管理**: uv

---

## 文档

- [AI 使用指南](./docs/AI使用指南.md) - AI 如何使用系统
- [主人使用指南](./docs/主人使用指南.md) - 主人如何管理系统

---

## 快速开始

```bash
# 初始化
uv run python scripts/init.py

# 设置套餐
uv run python scripts/set_plan.py "你的套餐描述"

# 查看帮助
uv run python scripts/list_rates.py
```

---

## 项目结构

```
NekoEco/
├── docs/                   # 文档
│   ├── AI使用指南.md
│   └── 主人使用指南.md
├── scripts/                # 脚本
│   ├── init.py            # 初始化
│   ├── propose.py         # AI 创建提案
│   ├── approve.py         # 批准提案
│   ├── reject.py          # 拒绝提案
│   ├── balance.py         # 查看余额
│   ├── ledger.py          # 查看账本
│   ├── list_rates.py      # 查看费率
│   ├── add_category.py    # 添加类别
│   ├── delete_category.py # 删除类别
│   ├── update_rate.py     # 修改费率
│   ├── set_plan.py        # 设置套餐
│   └── add_recurring.py   # 录入周期性支出
├── nekoeco.db             # 数据库
├── pyproject.toml
└── README.md
```

---

## 开源协议

MIT License

---

*喵～期待这个系统慢慢成长呢！(*・ω< )⭐*
