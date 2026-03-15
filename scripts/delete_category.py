#!/usr/bin/env python3
"""删除类别"""

import sqlite3
import os
import sys

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nekoeco.db")


def delete_category(category_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 查找类别
    cursor.execute(
        "SELECT id, name, type FROM categories WHERE name = ?", (category_name,)
    )
    category = cursor.fetchone()

    if not category:
        conn.close()
        print(f"错误: 类别 '{category_name}' 不存在")
        sys.exit(1)

    cat_id, name, ctype = category

    # 检查是否有交易记录
    cursor.execute(
        "SELECT COUNT(*) FROM transactions WHERE category = ?", (category_name,)
    )
    count = cursor.fetchone()[0]

    if count > 0:
        conn.close()
        print(f"错误: 类别 '{name}' 已有 {count} 笔交易记录，无法删除")
        sys.exit(1)

    # 删除费率
    cursor.execute("DELETE FROM rates WHERE category_id = ?", (cat_id,))

    # 删除类别
    cursor.execute("DELETE FROM categories WHERE id = ?", (cat_id,))

    conn.commit()
    conn.close()

    print(f"类别 '{name}' 已删除")


def main():
    if len(sys.argv) != 2:
        print("用法: python delete_category.py <类别名称>")
        print()
        print("示例: python delete_category.py 测试类别")
        print("注意: 有交易记录的类别无法删除")
        sys.exit(1)

    category_name = sys.argv[1]
    delete_category(category_name)


if __name__ == "__main__":
    main()
