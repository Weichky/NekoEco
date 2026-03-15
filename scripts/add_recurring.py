#!/usr/bin/env python3
"""手动录入周期性支出"""

import sqlite3
import os
import sys
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nekoeco.db")


def add_recurring_expense(name, amount):
    if amount <= 0:
        print("错误: 金额必须大于 0")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "INSERT INTO transactions (proposal_id, type, category, amount, description, executed_at) VALUES (?, ?, ?, ?, ?, ?)",
        (None, "expense", name, amount, "周期性支出", now),
    )

    cursor.execute(
        "UPDATE balance SET nt_balance = nt_balance - ? WHERE id = 1", (amount,)
    )

    cursor.execute("SELECT nt_balance FROM balance WHERE id = 1")
    new_balance = cursor.fetchone()[0]

    conn.commit()
    conn.close()

    print(f"已录入支出: {name}")
    print(f"  金额: {amount} NT")
    print(f"  当前余额: {new_balance} NT")


def main():
    if len(sys.argv) != 3:
        print("用法: python add_recurring.py <项目名称> <金额>")
        print()
        print("示例: python add_recurring.py MiniMax Max 月费 11.9")
        sys.exit(1)

    name = sys.argv[1]

    try:
        amount = float(sys.argv[2])
    except ValueError:
        print("错误: 金额必须是数字")
        sys.exit(1)

    add_recurring_expense(name, amount)


if __name__ == "__main__":
    main()
