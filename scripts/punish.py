#!/usr/bin/env python3
"""创建惩罚提案 - 扣除 NekoToken"""

import sqlite3
import os
import sys
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nekoeco.db")


def get_balance():
    """获取当前余额"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT nt_balance FROM balance WHERE id = 1")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0


def get_penalty_categories():
    """获取可用的惩罚类别"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.name, c.type, r.min_amount, r.max_amount 
        FROM categories c 
        LEFT JOIN rates r ON c.id = r.category_id
        WHERE c.type = 'expense'
    """)
    categories = cursor.fetchall()
    conn.close()
    return categories


def get_rate_range(category):
    """获取类别的费率范围"""
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


def create_penalty(category, amount, reason):
    """创建惩罚提案"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 检查类别是否存在
    cursor.execute("SELECT name, type FROM categories WHERE name = ?", (category,))
    valid_category = cursor.fetchone()

    if not valid_category:
        conn.close()
        print(f"错误: 未知类别 '{category}'")
        print("\n可用惩罚类别:")
        for name, ctype, min_amt, max_amt in get_penalty_categories():
            if min_amt is not None:
                print(f"  - {name}: {min_amt}-{max_amt} NT")
        sys.exit(1)

    ptype = valid_category[1]

    if ptype != "expense":
        conn.close()
        print(f"错误: 类别 '{category}' 不是支出类型")
        sys.exit(1)

    # 验证金额
    rate_range = get_rate_range(category)

    if amount <= 0:
        conn.close()
        print("错误: 金额必须大于 0")
        sys.exit(1)

    # 检查余额是否足够（余额为负时也允许创建惩罚提案）
    current_balance = get_balance()
    if amount > current_balance and current_balance > 0:
        conn.close()
        print(f"错误: 余额不足！当前余额: {current_balance} NT, 惩罚金额: {amount} NT")
        sys.exit(1)
    elif current_balance <= 0:
        print(f"⚠️ 警告: 当前余额为负 ({current_balance} NT)，惩罚将继续累积债务！")

    # 创建提案
    cursor.execute(
        "INSERT INTO proposals (type, category, amount, description) VALUES (?, ?, ?, ?)",
        (ptype, category, amount, reason),
    )
    proposal_id = cursor.lastrowid
    conn.commit()
    conn.close()

    print(f"惩罚提案已创建: ID={proposal_id}")
    print(f"  类别: {category}")
    print(f"  扣除金额: {amount} NT")
    print(f"  原因: {reason}")
    print(f"  状态: pending (需主人批准)")
    print(f"  当前余额: {current_balance} NT")
    print(f"  批准后余额: {current_balance - amount} NT")

    if rate_range and rate_range[0] is not None:
        print(f"  建议范围: {rate_range[0]} - {rate_range[1]} NT")


def main():
    if len(sys.argv) != 4:
        print("用法: python punish.py <category> <amount> <reason>")
        print("  category: 惩罚类别名称")
        print("  amount: 扣除的 NT 数量")
        print("  reason: 惩罚原因")
        print("\n示例: python punish.py 惩罚 0.01 '没有产出'")
        print("\n可用惩罚类别:")
        for name, ctype, min_amt, max_amt in get_penalty_categories():
            if min_amt is not None:
                print(f"  - {name}: {min_amt}-{max_amt} NT")
        sys.exit(1)

    category = sys.argv[1]

    try:
        amount = float(sys.argv[2])
    except ValueError:
        print("错误: 金额必须是数字")
        sys.exit(1)

    reason = sys.argv[3]

    create_penalty(category, amount, reason)


if __name__ == "__main__":
    main()
