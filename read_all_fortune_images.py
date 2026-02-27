#!/usr/bin/env python3
"""
批量读取所有签文图片并记录实际签级
需要手动查看图片并输入签级
"""

import json
from pathlib import Path

# 已经确认的签级（从图片中读取）
CONFIRMED_LEVELS = {
    1: "大吉",
    9: "大吉",
    17: "凶",
    29: "凶",  # 需要再次确认
    48: "小吉",
    60: "小吉",
    94: "半吉",
    100: "凶",
}

def display_all_images():
    """显示所有签的图片路径，供手动查看"""

    print("=" * 80)
    print("请按顺序查看每个签的图片，记录签级")
    print("=" * 80)
    print()

    for i in range(1, 101):
        image_path = f"omikuji/data/senso-ji-omikuji-main/{i}_0.jpg"
        confirmed = CONFIRMED_LEVELS.get(i, "?")
        print(f"第 {i:3d} 签: {image_path:50s} [{confirmed}]")

    print()
    print("=" * 80)
    print("提示：在Mac上可以使用以下命令批量查看：")
    print("  open omikuji/data/senso-ji-omikuji-main/*_0.jpg")

def batch_read_with_tool():
    """使用Claude的Read工具批量读取图片"""

    print("建议使用以下方式批量验证：")
    print()
    print("1. 分批读取图片（每批10个）")
    print("2. 记录每个签的实际签级")
    print("3. 使用update_fortunes_from_manual_input()更新数据")
    print()

    # 分组建议
    groups = [
        (1, 10, "第1-10签"),
        (11, 20, "第11-20签"),
        (21, 30, "第21-30签"),
        (31, 40, "第31-40签"),
        (41, 50, "第41-50签"),
        (51, 60, "第51-60签"),
        (61, 70, "第61-70签"),
        (71, 80, "第71-80签"),
        (81, 90, "第81-90签"),
        (91, 100, "第91-100签"),
    ]

    for start, end, name in groups:
        print(f"\n### {name}")
        for i in range(start, end + 1):
            print(f"Read('/Users/leayn/Documents/PythonProject/yinian/omikuji/data/senso-ji-omikuji-main/{i}_0.jpg')")

def update_fortunes_from_dict(levels_dict):
    """从字典更新签文数据"""

    json_file = "omikuji/data/senso-ji-fortunes-full.json"
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    fixed_count = 0
    for fortune in data['fortunes']:
        fortune_id = fortune['id']
        if fortune_id in levels_dict:
            correct_level = levels_dict[fortune_id]
            if fortune['level'] != correct_level:
                old_level = fortune['level']
                fortune['level'] = correct_level
                print(f"✓ 第 {fortune_id:3d} 签: {old_level:4s} → {correct_level}")
                fixed_count += 1

    if fixed_count > 0:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 修复了 {fixed_count} 个签")
    else:
        print("\n无需修复")

if __name__ == "__main__":
    print("签文图片批量读取工具")
    print()
    print("选项：")
    print("  1. 显示所有图片路径")
    print("  2. 显示分批读取建议")
    print("  3. 使用已确认的签级更新")
    print()

    choice = input("请选择 (1/2/3): ").strip()

    if choice == '1':
        display_all_images()
    elif choice == '2':
        batch_read_with_tool()
    elif choice == '3':
        print("\n使用已确认的签级更新：")
        print(f"共 {len(CONFIRMED_LEVELS)} 个已确认签级")
        update_fortunes_from_dict(CONFIRMED_LEVELS)
    else:
        print("无效选择")
