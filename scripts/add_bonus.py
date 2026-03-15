#!/usr/bin/env python3
"""追加奖励 - 给已存在的提案添加额外奖励"""

import sqlite3
import os
import sys
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nekoeco.db")


def add_bonus(proposal_id, amount, description):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 检查提案是否存在
    cursor.execute(
        "SELECT id, type, category, amount, description, status FROM proposals WHERE id = ?",
        (proposal_id,),
    )
    proposal = cursor.fetchone()

    if not proposal:
        conn.close()
        print(f"错误: 提案 {proposal_id} 不存在")
        sys.exit(1)

    pid, ptype, category, original_amount, original_desc, status = proposal

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 更新原提案状态为 approved
    cursor.execute(
        "UPDATE proposals SET status = 'approved', decided_at = ? WHERE id = ?",
        (now, proposal_id),
    )

    # 写入原提案的交易
    cursor.execute(
        "INSERT INTO transactions (proposal_id, type, category, amount, description, executed_at) VALUES (?, ?, ?, ?, ?, ?)",
        (proposal_id, ptype, category, original_amount, original_desc, now),
    )

    # 更新余额（原提案）
    if ptype == "income":
        cursor.execute(
            "UPDATE balance SET nt_balance = nt_balance + ? WHERE id = 1",
            (original_amount,),
        )
    else:
        cursor.execute(
            "UPDATE balance SET nt_balance = nt_balance - ? WHERE id = 1",
            (original_amount,),
        )

    # 写入奖金交易（bonus 类型）
    bonus_category = "奖金"
    cursor.execute(
        "INSERT INTO transactions (proposal_id, type, category, amount, description, executed_at) VALUES (?, ?, ?, ?, ?, ?)",
        (proposal_id, "bonus", bonus_category, amount, description, now),
    )

    # 更新余额（奖金）
    cursor.execute(
        "UPDATE balance SET nt_balance = nt_balance + ? WHERE id = 1",
        (amount,),
    )

    conn.commit()

    # 获取更新后的余额
    cursor.execute("SELECT nt_balance FROM balance WHERE id = 1")
    new_balance = cursor.fetchone()[0]

    conn.close()

    print(f"提案 {proposal_id} 已批准")
    print(f"  原提案 - 类别: {category}, 金额: {original_amount} NT")
    print(f"  追加奖励 - 金额: {amount} NT")
    print(f"  描述: {description}")
    print(f"  当前余额: {new_balance} NT")


def main():
    if len(sys.argv) != 4:
        print("用法: python add_bonus.py <proposal_id> <amount> <description>")
        print("  proposal_id: 提案ID")
        print("  amount: 追加奖励金额")
        print("  description: 奖励描述")
        print("\n示例: python add_bonus.py 1 0.01 '主人觉得咱太可爱了！'")
        sys.exit(1)

    try:
        proposal_id = int(sys.argv[1])
    except ValueError:
        print("错误: proposal_id 必须是数字")
        sys.exit(1)

    try:
        amount = float(sys.argv[2])
    except ValueError:
        print("错误: amount 必须是数字")
        sys.exit(1)

    if amount <= 0:
        print("错误: 金额必须大于 0")
        sys.exit(1)

    description = sys.argv[3]

    add_bonus(proposal_id, amount, description)


if __name__ == "__main__":
    main()
