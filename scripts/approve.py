#!/usr/bin/env python3
"""批准提案"""

import sqlite3
import os
import sys
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nekoeco.db")


def approve_proposal(proposal_id, rate_min=None, rate_max=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 检查提案是否存在
    cursor.execute(
        "SELECT id, type, category, amount, description, status FROM proposals WHERE id = ?",
        (proposal_id,),
    )
    proposal = cursor.fetchone()

    if not proposal:
        conn.close()
        print(f"错误: 提案 {proposal_id} 不存在")
        sys.exit(1)

    pid, ptype, category, amount, description, status = proposal

    if status != "pending":
        conn.close()
        print(f"错误: 提案已经是 {status} 状态")
        sys.exit(1)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 更新提案状态
    cursor.execute(
        "UPDATE proposals SET status = ?, decided_at = ? WHERE id = ?",
        ("approved", now, proposal_id),
    )

    # 处理 category_add 类型
    if ptype == "category_add":
        if rate_min is None or rate_max is None:
            conn.close()
            print(f"错误: 批准类别提案需要指定费率范围")
            print(
                "用法: python approve.py <id> --rate-min <最小值> --rate-max <最大值>"
            )
            sys.exit(1)

        if rate_min <= 0 or rate_max <= 0:
            conn.close()
            print("错误: 费率必须大于 0")
            sys.exit(1)

        if rate_min > rate_max:
            conn.close()
            print("错误: 最小值不能大于最大值")
            sys.exit(1)

        # 写入 categories
        cursor.execute(
            "INSERT INTO categories (name, type) VALUES (?, ?)",
            (category, description),  # description 实际是 type
        )
        cat_id = cursor.lastrowid

        # 写入 rates
        cursor.execute(
            "INSERT INTO rates (category_id, min_amount, max_amount) VALUES (?, ?, ?)",
            (cat_id, rate_min, rate_max),
        )

        conn.commit()
        conn.close()

        print(f"类别 {category} 已添加")
        print(f"  类型: {description}")
        print(f"  费率: {rate_min} - {rate_max} NT")
        return

    # 写入交易记录
    cursor.execute(
        "INSERT INTO transactions (proposal_id, type, category, amount, description, executed_at) VALUES (?, ?, ?, ?, ?, ?)",
        (proposal_id, ptype, category, amount, description, now),
    )

    # 更新余额
    if ptype == "income":
        cursor.execute(
            "UPDATE balance SET nt_balance = nt_balance + ? WHERE id = 1", (amount,)
        )
    else:
        cursor.execute(
            "UPDATE balance SET nt_balance = nt_balance - ? WHERE id = 1", (amount,)
        )

    conn.commit()

    # 获取更新后的余额
    cursor.execute("SELECT nt_balance FROM balance WHERE id = 1")
    new_balance = cursor.fetchone()[0]

    conn.close()

    print(f"提案 {proposal_id} 已批准")
    print(f"  类型: {ptype}")
    print(f"  类别: {category}")
    print(f"  金额: {amount} NT")
    print(f"  描述: {description}")
    print(f"  当前余额: {new_balance} NT")


def main():
    rate_min = None
    rate_max = None

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--rate-min" and i + 1 < len(args):
            try:
                rate_min = float(args[i + 1])
            except ValueError:
                print("错误: --rate-min 必须是数字")
                sys.exit(1)
            i += 2
        elif args[i] == "--rate-max" and i + 1 < len(args):
            try:
                rate_max = float(args[i + 1])
            except ValueError:
                print("错误: --rate-max 必须是数字")
                sys.exit(1)
            i += 2
        else:
            i += 1

    # 提取 proposal_id（第一个非选项参数）
    proposal_id = None
    for arg in args:
        if not arg.startswith("--"):
            try:
                proposal_id = int(arg)
                break
            except ValueError:
                pass

    if proposal_id is None:
        print(
            "用法: python approve.py <proposal_id> [--rate-min <值>] [--rate-max <值>]"
        )
        print("示例: python approve.py 1")
        print("示例（类别提案）: python approve.py 1 --rate-min 10 --rate-max 100")
        sys.exit(1)

    approve_proposal(proposal_id, rate_min, rate_max)


if __name__ == "__main__":
    main()
