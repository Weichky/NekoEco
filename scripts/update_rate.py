#!/usr/bin/env python3
"""修改类别费率"""

import sqlite3
import os
import sys

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nekoeco.db")


def update_rate(category_name, new_min, new_max):
    if new_min <= 0 or new_max <= 0:
        print("错误: 费率必须大于 0")
        sys.exit(1)

    if new_min > new_max:
        print("错误: 最小值不能大于最大值")
        sys.exit(1)

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

    # 查找费率
    cursor.execute("SELECT id FROM rates WHERE category_id = ?", (cat_id,))
    rate = cursor.fetchone()

    if not rate:
        conn.close()
        print(f"错误: 类别 '{name}' 还没有费率，请先审批添加类别")
        sys.exit(1)

    # 更新费率
    cursor.execute(
        "UPDATE rates SET min_amount = ?, max_amount = ? WHERE category_id = ?",
        (new_min, new_max, cat_id),
    )
    conn.commit()
    conn.close()

    print(f"费率已更新: {name}")
    print(f"  类型: {ctype}")
    print(f"  旧费率: 查看 list_rates.py")
    print(f"  新费率: {new_min} - {new_max} NT")


def main():
    if len(sys.argv) != 4:
        print("用法: python update_rate.py <类别名称> <最小值> <最大值>")
        print()
        print("示例: python update_rate.py 创新项目 20 200")
        print("示例: python update_rate.py API调用费用 10 300")
        sys.exit(1)

    category_name = sys.argv[1]

    try:
        new_min = float(sys.argv[2])
        new_max = float(sys.argv[3])
    except ValueError:
        print("错误: 最小值和最大值必须是数字")
        sys.exit(1)

    update_rate(category_name, new_min, new_max)


if __name__ == "__main__":
    main()
