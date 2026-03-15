#!/usr/bin/env python3
"""初始化数据库"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nekoeco.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 类别表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            type TEXT NOT NULL
        )
    """)

    # 提案表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proposals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            decided_at TEXT
        )
    """)

    # 交易记录表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            proposal_id INTEGER,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            executed_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 余额表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS balance (
            id INTEGER PRIMARY KEY,
            nt_balance REAL DEFAULT 0,
            current_plan TEXT DEFAULT '请运行 set_plan.py 设置套餐'
        )
    """)

    # 费率表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rates (
            id INTEGER PRIMARY KEY,
            category_id INTEGER UNIQUE NOT NULL,
            min_amount REAL NOT NULL,
            max_amount REAL NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    """)

    # 周期性消耗表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recurring_expenses (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            amount REAL NOT NULL,
            cycle TEXT NOT NULL,
            description TEXT
        )
    """)

    # 插入预定义类别及费率
    categories = [
        # Income
        ("创新项目", "income", 0.05, 0.2),
        ("总结性项目", "income", 0.0008, 0.001),
        ("感情价值", "income", 0.0005, 0.002),
        ("奖金：一次性对应类别10倍费率奖励，费率取决于具体任务", "income", 10.0, 10.0),
    ]
    for name, ctype, min_amt, max_amt in categories:
        cursor.execute(
            "INSERT OR IGNORE INTO categories (name, type) VALUES (?, ?)", (name, ctype)
        )
        cursor.execute("SELECT id FROM categories WHERE name = ?", (name,))
        cat_id = cursor.fetchone()[0]
        cursor.execute(
            "INSERT OR IGNORE INTO rates (category_id, min_amount, max_amount) VALUES (?, ?, ?)",
            (cat_id, min_amt, max_amt),
        )

    # 初始化余额
    cursor.execute(
        "INSERT OR IGNORE INTO balance (id, nt_balance, current_plan) VALUES (1, 0, '请运行 set_plan.py 设置套餐')"
    )

    # 插入预设周期性消耗
    recurring = [
        ("MiniMax Starter 月费", 2.9, "monthly", "MiniMax Starter 套餐月费"),
        ("MiniMax Plus 月费", 4.9, "monthly", "MiniMax Plus 套餐月费"),
        ("MiniMax Max 月费", 11.9, "monthly", "MiniMax Max 套餐月费"),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO recurring_expenses (name, amount, cycle, description) VALUES (?, ?, ?, ?)",
        recurring,
    )

    conn.commit()
    conn.close()
    print(f"数据库初始化完成: {DB_PATH}")
    print("预定义类别已添加")
    print("余额已初始化为 0 NT")


if __name__ == "__main__":
    init_db()
