#!/usr/bin/env python3
"""查看待批准的提案"""

import sqlite3
import os
import sys

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nekoeco.db")


def list_pending():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, category, type, amount, description, created_at 
        FROM proposals 
        WHERE status = 'pending' 
        ORDER BY id
    """)
    pending = cursor.fetchall()
    conn.close()

    if not pending:
        print("当前没有待批准的提案")
        return

    print("=" * 60)
    print("待批准的提案")
    print("=" * 60)
    print(f"{'ID':<4} {'类别':<12} {'类型':<8} {'金额':<10} {'描述':<20}")
    print("-" * 60)
    
    for p in pending:
        pid, category, ptype, amount, description, created_at = p
        desc = description[:18] + ".." if description and len(description) > 20 else (description or "")
        print(f"{pid:<4} {category:<12} {ptype:<8} {amount:<10.4f} {desc:<20}")
    
    print("-" * 60)
    print(f"共 {len(pending)} 个待批准提案")
    print("\n使用方法:")
    print("  批准提案: python scripts/approve.py <id>")
    print("  拒绝提案: python scripts/reject.py <id>")


def main():
    list_pending()


if __name__ == "__main__":
    main()
