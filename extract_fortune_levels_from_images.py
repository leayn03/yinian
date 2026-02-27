#!/usr/bin/env python3
"""
从签文图片中提取签级信息
由于图片识别需要手动确认，这个脚本提供交互式界面
"""

import json
from pathlib import Path

def manual_verify_fortunes():
    """手动验证每个签的签级"""

    # 读取当前数据
    json_file = "omikuji/data/senso-ji-fortunes-full.json"
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("🔍 手动验证签文签级")
    print("=" * 60)
    print("请查看图片文件，输入实际签级")
    print("可选签级：大吉、吉、半吉、小吉、末吉、凶、大凶")
    print("输入 's' 跳过，输入 'q' 退出")
    print("=" * 60)
    print()

    corrections = []

    for fortune in data['fortunes']:
        fortune_id = fortune['id']
        current_level = fortune['level']
        image_path = f"omikuji/data/senso-ji-omikuji-main/{fortune_id}_0.jpg"

        print(f"\n签号 {fortune_id:3d}")
        print(f"  图片：{image_path}")
        print(f"  当前签级：{current_level}")

        # 在这里你需要查看图片
        user_input = input(f"  实际签级 (回车=保持不变): ").strip()

        if user_input.lower() == 'q':
            break
        elif user_input.lower() == 's' or user_input == '':
            continue
        elif user_input in ['大吉', '吉', '半吉', '小吉', '末吉', '凶', '大凶']:
            if user_input != current_level:
                corrections.append({
                    'id': fortune_id,
                    'old': current_level,
                    'new': user_input
                })
                fortune['level'] = user_input
                print(f"  ✓ 已更新：{current_level} → {user_input}")
        else:
            print(f"  ✗ 无效签级，跳过")

    if corrections:
        print("\n" + "=" * 60)
        print(f"共修改了 {len(corrections)} 个签：")
        for corr in corrections:
            print(f"  签号 {corr['id']:3d}: {corr['old']} → {corr['new']}")

        save = input("\n是否保存修改？(y/N): ").strip().lower()
        if save == 'y':
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("✅ 已保存")
        else:
            print("❌ 已取消")
    else:
        print("\n无修改")

def quick_fix_known_issues():
    """快速修复已知的问题签"""

    print("🔧 快速修复已知问题")
    print("=" * 60)

    # 已知需要修复的签（基于图片实际内容）
    # 这里需要你提供实际查看图片后的结果
    known_fixes = {
        9: "大吉",  # 图片显示"第九 大吉"
        # 在这里添加其他需要修复的签
    }

    json_file = "omikuji/data/senso-ji-fortunes-full.json"
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    fixed_count = 0
    for fortune in data['fortunes']:
        fortune_id = fortune['id']
        if fortune_id in known_fixes:
            correct_level = known_fixes[fortune_id]
            if fortune['level'] != correct_level:
                old_level = fortune['level']
                fortune['level'] = correct_level
                print(f"✓ 签号 {fortune_id:3d}: {old_level} → {correct_level}")
                fixed_count += 1

    if fixed_count > 0:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 修复了 {fixed_count} 个签")
    else:
        print("\n无需修复")

if __name__ == "__main__":
    import sys

    print("请选择模式：")
    print("  1) 快速修复已知问题（第9签等）")
    print("  2) 手动验证所有签（交互式）")
    print()

    choice = input("请选择 (1/2): ").strip()

    if choice == '1':
        quick_fix_known_issues()
    elif choice == '2':
        manual_verify_fortunes()
    else:
        print("无效选择")
