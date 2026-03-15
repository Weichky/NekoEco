#!/usr/bin/env python3
"""查看费率"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nekoeco.db")


def list_rates():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 收入类别费率
    cursor.execute("""
        SELECT c.name, c.type, r.min_amount, r.max_amount
        FROM categories c
        INNER JOIN rates r ON c.id = r.category_id
        WHERE c.type = 'income'
        ORDER BY c.name
    """)
    income_rates = cursor.fetchall()

    # 周期性消耗
    cursor.execute("""
        SELECT name, amount, cycle, description
        FROM recurring_expenses
        ORDER BY amount
    """)
    recurring = cursor.fetchall()

    conn.close()

    # 收入类别
    print("=" * 50)
    print("收入类别")
    print("=" * 50)
    if income_rates:
        for name, _, min_amt, max_amt in income_rates:
            if min_amt == max_amt:
                print(f"  {name}: {min_amt} NT")
            else:
                print(f"  {name}: {min_amt} - {max_amt} NT")
    else:
        print("  暂无")

    # 周期性消耗
    print()
    print("=" * 50)
    print("周期性消耗（由主人手动录入）")
    print("=" * 50)
    if recurring:
        cycle_names = {"monthly": "月", "weekly": "周", "daily": "日"}
        for name, amount, cycle, desc in recurring:
            cycle_name = cycle_names.get(cycle, cycle)
            print(f"  {name}: {amount} NT/{cycle_name}")
            if desc:
                print(f"    ({desc})")
    else:
        print("  暂无")


if __name__ == "__main__":
    list_rates()
