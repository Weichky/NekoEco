#!/usr/bin/env python3
"""查看余额"""

import sqlite3
import os
import sys

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nekoeco.db")


def show_balance():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT nt_balance, current_plan FROM balance WHERE id = 1")
    result = cursor.fetchone()

    conn.close()

    if result:
        balance, current_plan = result
        print(f"当前套餐: {current_plan}")
        print(f"余额: {balance} NT")

        if balance < 0:
            print()
            print("⚠️ 余额为负！可能触发服务降级")
    else:
        print("余额未初始化，请先运行 init.py")


def main():
    show_balance()


if __name__ == "__main__":
    main()
