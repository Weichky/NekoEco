#!/usr/bin/env python3
"""创建提案 - AI 调用"""

import sqlite3
import os
import sys

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nekoeco.db")


def get_categories():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.name, c.type, r.min_amount, r.max_amount 
        FROM categories c 
        LEFT JOIN rates r ON c.id = r.category_id
        WHERE c.type = 'income'
    """)
    categories = cursor.fetchall()
    conn.close()
    return categories


def get_rate_range(category):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT r.min_amount, r.max_amount 
        FROM categories c 
        LEFT JOIN rates r ON c.id = r.category_id
        WHERE c.name = ?
    """,
        (category,),
    )
    result = cursor.fetchone()
    conn.close()
    return result  # (min, max) or None


def create_proposal(category, amount, description):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name, type FROM categories WHERE name = ?", (category,))
    valid_category = cursor.fetchone()

    if not valid_category:
        conn.close()
        print(f"错误: 未知类别 '{category}'")
        print("可用类别:")
        for name, ctype, min_amt, max_amt in get_categories():
            if min_amt is not None:
                print(f"  - {name}: {min_amt}-{max_amt} NT")
        sys.exit(1)

    proposal_type = valid_category[1]

    rate_range = get_rate_range(category)

    if amount <= 0:
        conn.close()
        print("错误: 金额必须大于 0")
        sys.exit(1)

    cursor.execute(
        "INSERT INTO proposals (type, category, amount, description) VALUES (?, ?, ?, ?)",
        (proposal_type, category, amount, description),
    )
    proposal_id = cursor.lastrowid
    conn.commit()
    conn.close()

    print(f"提案已创建: ID={proposal_id}")
    print(f"  类别: {category}")
    print(f"  金额: {amount} NT")
    print(f"  描述: {description}")
    print(f"  状态: pending")

    if rate_range and rate_range[0] is not None:
        print(f"  建议范围: {rate_range[0]} - {rate_range[1]} NT")
        if amount < rate_range[0]:
            print(f"  ⚠️ 金额低于建议最小值")
        elif amount > rate_range[1]:
            print(f"  ⚠️ 金额超过建议最大值")


def main():
    if len(sys.argv) != 4:
        print("用法: python propose.py <category> <amount> <description>")
        print("  category: 类别名称")
        print("  amount: NT 数量")
        print("  description: 描述")
        print("\n示例: python propose.py 创新项目 0.15 '协助完成项目'")
        print("\n可用类别:")
        for name, ctype, min_amt, max_amt in get_categories():
            if min_amt is not None:
                print(f"  - {name}: {min_amt}-{max_amt} NT")
        sys.exit(1)

    category = sys.argv[1]

    try:
        amount = float(sys.argv[2])
    except ValueError:
        print("错误: 金额必须是数字")
        sys.exit(1)

    description = sys.argv[3]

    create_proposal(category, amount, description)


if __name__ == "__main__":
    main()
