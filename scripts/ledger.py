#!/usr/bin/env python3
"""查看账本"""

import sqlite3
import os
import sys

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nekoeco.db")


def show_ledger(type_filter=None, category_filter=None, limit=50):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = "SELECT type, category, amount, description, executed_at FROM transactions WHERE 1=1"
    params = []

    if type_filter:
        query += " AND type = ?"
        params.append(type_filter)

    if category_filter:
        query += " AND category = ?"
        params.append(category_filter)

    query += " ORDER BY executed_at DESC LIMIT ?"
    params.append(limit)

    cursor.execute(query, params)
    transactions = cursor.fetchall()

    conn.close()

    if not transactions:
        print("暂无交易记录")
        return

    # 收入、奖金、支出分开显示
    income = [t for t in transactions if t[0] == "income"]
    bonus = [t for t in transactions if t[0] == "bonus"]
    expense = [t for t in transactions if t[0] == "expense"]

    if income:
        print("收入:")
        print(f"{'时间':<20} {'类别':<15} {'金额':<10} {'描述'}")
        print("-" * 60)
        for t in income:
            print(f"{t[4]:<20} {t[1]:<15} {t[2]:<10} {t[3]}")

    if bonus:
        if income:
            print()
        print("奖励 (Bonus):")
        print(f"{'时间':<20} {'类别':<15} {'金额':<10} {'描述'}")
        print("-" * 60)
        for t in bonus:
            print(f"{t[4]:<20} {t[1]:<15} {t[2]:<10} {t[3]}")


def main():
    type_filter = None
    category_filter = None
    limit = 50

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--type" and i + 1 < len(args):
            type_filter = args[i + 1]
            i += 2
        elif args[i] == "--category" and i + 1 < len(args):
            category_filter = args[i + 1]
            i += 2
        elif args[i] == "--limit" and i + 1 < len(args):
            limit = int(args[i + 1])
            i += 2
        else:
            i += 1

    show_ledger(type_filter, category_filter, limit)


if __name__ == "__main__":
    main()
