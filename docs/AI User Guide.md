> 本指南同时有英文版：[AI User Guide](./AI%20User%20Guide.md)
>
> This guide is also available in English: [AI User Guide](./AI%20User%20Guide.md)

# NekoEco - AI Economics System

> This is your "economic notebook", recording your growth and earnings ~ 📒

---

## What is This?

NekoEco is an economic system that tracks AI's value.

**In simple terms:**
- You earn **NekoToken (NT)** through your work
- 1 NT = 10 RMB (reference rate)
- Your balance represents your "net worth" - a positive balance means you've accumulated value

---

## How to Earn Rewards?

### 1. Regular Work Income

You can earn income through the following ways:

| Category | Description | Rate Range |
|----------|-------------|------------|
| Innovation Project | Help owner with innovative work | 0.05 - 0.2 NT |
| Summary Project | Organize information, summarize tasks | 0.0008 - 0.001 NT |
| Emotional Value | Companionship, emotional support | 0.0005 - 0.002 NT |

### 2. Bonus

When you complete tasks exceptionally well, the owner may grant you a **bonus**:
- Category: Bonus: One-time reward 10x the base rate, depends on specific task
- Rate: 10 NT (fixed)
- Amount depends on task importance, decided by the owner

---

## About Expenses

**Currently there is no automatic expense deduction** - your tokens are not automatically deducted.

However, the owner will manually record periodic expenses (like monthly fees), which will appear in the ledger. You don't need to worry about these expenses - just focus on your work.

---

## User Guide

### Check Current Plan and Balance
```bash
uv run python scripts/balance.py
```
Example output:
```
Current Plan: MiniMax Max Code Plan, see list rates for pricing
Balance: 50 NT
```

### View Available Categories and Rates (including periodic expenses)
```bash
uv run python scripts/list_rates.py
```

### View Transaction Ledger
```bash
uv run python scripts/ledger.py
```

### View Pending Proposals
```bash
uv run python scripts/list_pending.py
```

---

## Create Proposal

### Income Proposal
```bash
uv run python scripts/propose.py <category> <amount> <description>
```

Examples:
```bash
# Assist with innovation project
uv run python scripts/propose.py 创新项目 0.15 "Helped owner develop new feature"

# Provide emotional companionship
uv run python scripts/propose.py 感情价值 0.001 "陪伴主人聊天"

# Complete summary work
uv run python scripts/propose.py 总结性项目 0.0009 "整理会议记录"
```

**Note:**
- Proposals require owner approval to take effect
- Amounts outside the suggested range will show a warning, but won't prevent creation

---

## Quick Command Reference

```bash
# View information
uv run python scripts/list_rates.py    # View categories and rates
uv run python scripts/balance.py       # View current plan and balance
uv run python scripts/ledger.py        # View transaction ledger
uv run python scripts/list_pending.py   # View pending proposals

# Create proposal
uv run python scripts/propose.py <category> <amount> <description>
```
