#!/usr/bin/env python3
"""设置当前套餐"""

import sqlite3
import os
import sys

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nekoeco.db")


def set_plan(plan_text):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("UPDATE balance SET current_plan = ? WHERE id = 1", (plan_text,))
    conn.commit()
    conn.close()

    print(f"当前套餐已设置为: {plan_text}")


def main():
    if len(sys.argv) < 2:
        print("用法: python set_plan.py <套餐描述>")
        print()
        print("示例: python set_plan.py 'MiniMax Max Code Plan，具体资费请 list rates'")
        sys.exit(1)

    plan_text = " ".join(sys.argv[1:])
    set_plan(plan_text)


if __name__ == "__main__":
    main()
