#!/usr/bin/env python3
"""拒绝提案"""

import sqlite3
import os
import sys
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nekoeco.db")


def reject_proposal(proposal_id):
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
        ("rejected", now, proposal_id),
    )

    conn.commit()
    conn.close()

    print(f"提案 {proposal_id} 已拒绝")
    print(f"  类型: {ptype}")
    print(f"  类别: {category}")
    print(f"  金额: {amount} NT")
    print(f"  描述: {description}")


def main():
    if len(sys.argv) != 2:
        print("用法: python reject.py <proposal_id>")
        print("示例: python reject.py 1")
        sys.exit(1)

    try:
        proposal_id = int(sys.argv[1])
    except ValueError:
        print("错误: proposal_id 必须是整数")
        sys.exit(1)

    reject_proposal(proposal_id)


if __name__ == "__main__":
    main()
