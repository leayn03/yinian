#!/usr/bin/env python3
"""
检查签文数据和图片的对应关系
"""

import json
import os
from pathlib import Path

def check_fortune_images():
    """检查所有签文的图片对应关系"""

    # 读取JSON数据
    json_file = "omikuji/data/senso-ji-fortunes-full.json"
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    fortunes = data['fortunes']

    # 图片目录
    image_dir = Path("omikuji/data/senso-ji-omikuji-main")

    print("🔍 检查签文数据和图片对应关系")
    print("=" * 60)

    errors = []
    warnings = []
    success_count = 0

    # 检查每个签
    for fortune in fortunes:
        fortune_id = fortune['id']
        image_front = fortune.get('imageFront', '')
        image_back = fortune.get('imageBack', '')

        # 预期的图片路径
        expected_front = f"senso-ji-omikuji-main/{fortune_id}_0.jpg"
        expected_back = f"senso-ji-omikuji-main/{fortune_id}_1.jpg"

        # 检查正面图片
        if image_front != expected_front:
            errors.append({
                'id': fortune_id,
                'type': 'front',
                'current': image_front,
                'expected': expected_front
            })

        # 检查背面图片
        if image_back != expected_back:
            errors.append({
                'id': fortune_id,
                'type': 'back',
                'current': image_back,
                'expected': expected_back
            })

        # 检查文件是否存在
        front_file = Path(image_front.replace('senso-ji-omikuji-main/', 'omikuji/data/senso-ji-omikuji-main/'))
        back_file = Path(image_back.replace('senso-ji-omikuji-main/', 'omikuji/data/senso-ji-omikuji-main/'))

        if not front_file.exists():
            warnings.append({
                'id': fortune_id,
                'type': 'missing_front',
                'file': str(front_file)
            })

        if not back_file.exists():
            warnings.append({
                'id': fortune_id,
                'type': 'missing_back',
                'file': str(back_file)
            })

        # 如果都正确
        if image_front == expected_front and image_back == expected_back:
            success_count += 1

    # 输出结果
    print(f"\n✅ 正确匹配：{success_count} 个签")

    if errors:
        print(f"\n❌ 发现 {len(errors)} 个路径错误：")
        print("-" * 60)
        for err in errors:
            print(f"签号 {err['id']} - {err['type']}面:")
            print(f"  当前：{err['current']}")
            print(f"  应为：{err['expected']}")
            print()

    if warnings:
        print(f"\n⚠️  发现 {len(warnings)} 个文件缺失：")
        print("-" * 60)
        for warn in warnings:
            print(f"签号 {warn['id']} - {warn['type']}:")
            print(f"  文件：{warn['file']}")
            print()

    if not errors and not warnings:
        print("\n🎉 所有签文数据和图片对应关系完全正确！")

    return errors, warnings

def fix_fortune_images(errors):
    """修复签文图片路径"""

    if not errors:
        print("\n✅ 无需修复")
        return

    print("\n🔧 开始修复...")

    # 读取JSON数据
    json_file = "omikuji/data/senso-ji-fortunes-full.json"
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 修复每个错误
    for err in errors:
        fortune_id = err['id']
        for fortune in data['fortunes']:
            if fortune['id'] == fortune_id:
                if err['type'] == 'front':
                    old_value = fortune['imageFront']
                    fortune['imageFront'] = err['expected']
                    print(f"✓ 签号 {fortune_id} 正面: {old_value} → {err['expected']}")
                elif err['type'] == 'back':
                    old_value = fortune['imageBack']
                    fortune['imageBack'] = err['expected']
                    print(f"✓ 签号 {fortune_id} 背面: {old_value} → {err['expected']}")

    # 保存修复后的数据
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 修复完成！已更新 {json_file}")

if __name__ == "__main__":
    errors, warnings = check_fortune_images()

    if errors:
        print("\n" + "=" * 60)
        choice = input("\n是否自动修复这些错误？(y/N): ").strip().lower()
        if choice == 'y':
            fix_fortune_images(errors)
            print("\n🎉 修复完成！请重新测试应用。")
        else:
            print("\n❌ 已取消修复")

    if warnings and not errors:
        print("\n⚠️  注意：有图片文件缺失，请检查图片目录")
