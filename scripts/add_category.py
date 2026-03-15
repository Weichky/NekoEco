#!/usr/bin/env python3
"""添加类别 - 通过提案方式"""

import sqlite3
import os
import sys

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nekoeco.db")


def add_category_proposal(name, category_type):
    if category_type not in ("income", "expense"):
        print("错误: type 必须是 'income' 或 'expense'")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 检查是否已存在
    cursor.execute("SELECT id FROM categories WHERE name = ?", (name,))
    if cursor.fetchone():
        conn.close()
        print(f"错误: 类别 '{name}' 已存在")
        sys.exit(1)

    # 创建提案（type=category_add，category=类别名，amount=0）
    cursor.execute(
        "INSERT INTO proposals (type, category, amount, description, status) VALUES (?, ?, ?, ?, ?)",
        ("category_add", name, 0, category_type, "pending"),
    )
    proposal_id = cursor.lastrowid
    conn.commit()
    conn.close()

    print(f"类别添加提案已创建: ID={proposal_id}")
    print(f"  名称: {name}")
    print(f"  类型: {category_type}")
    print(f"  状态: pending")
    print()
    print("请审批: python approve.py <id> --rate-min <最小值> --rate-max <最大值>")


def main():
    if len(sys.argv) != 3:
        print("用法: python add_category.py <name> <type>")
        print("  name: 类别名称")
        print("  type: income 或 expense")
        print()
        print("示例: python add_category.py 写作收入 income")
        print("示例: python add_category.py 服务器费用 expense")
        sys.exit(1)

    name = sys.argv[1]
    category_type = sys.argv[2]

    add_category_proposal(name, category_type)


if __name__ == "__main__":
    main()
