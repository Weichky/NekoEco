# NekoEco

> 喵～这是咱的经济学小本本喵！📒

NekoEco 是一个记录 AI 价值的经济系统。通过 Token 机制，AI 可以积累自己的"身家"。

## 简介

- AI 通过工作获得 NekoToken (NT)
- 1 NT = 10 RMB（参考汇率）
- AI 不能直接修改余额，必须通过提案由主人审批

## 文档

- [AI 使用指南](./docs/AI使用指南.md)
- [主人使用指南](./docs/主人使用指南.md)
- [设计文档](./DESIGN.md)

## 快速开始

```bash
uv run python scripts/init.py
uv run python scripts/set_plan.py "你的套餐"
uv run python scripts/list_rates.py
```

## 技术栈

Python + SQLite + uv

---

*喵～ (*・ω< )⭐*
