#!/usr/bin/env python3
"""查看可用类别"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nekoeco.db")


def list_categories():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, type FROM categories ORDER BY type, name")
    categories = cursor.fetchall()
    conn.close()

    income = [c for c in categories if c[1] == "income"]
    expense = [c for c in categories if c[1] == "expense"]

    print("可用类别:")
    print()

    if income:
        print("收入 (income):")
        for name, _ in income:
            print(f"  - {name}")

    if expense:
        print()
        print("支出 (expense):")
        for name, _ in expense:
            print(f"  - {name}")


if __name__ == "__main__":
    list_categories()
