#!/usr/bin/env python3
"""
验证签文签级是否与浅草寺官方签级对应
根据浅草寺100签的官方签级分布进行验证
"""

import json

# 浅草寺100签的官方签级对照表
# 数据来源：https://github.com/fumiama/senso-ji-omikuji
SENSO_JI_FORTUNE_LEVELS = {
    # 大吉 (17个)
    1: "大吉", 2: "大吉", 3: "大吉", 5: "大吉", 7: "大吉",
    8: "大吉", 11: "大吉", 12: "大吉", 14: "大吉", 24: "大吉",
    32: "大吉", 41: "大吉", 42: "大吉", 51: "大吉", 52: "大吉",
    64: "大吉", 100: "大吉",

    # 吉 (35个)
    4: "吉", 6: "吉", 10: "吉", 13: "吉", 15: "吉",
    16: "吉", 20: "吉", 21: "吉", 22: "吉", 23: "吉",
    25: "吉", 26: "吉", 28: "吉", 30: "吉", 31: "吉",
    33: "吉", 34: "吉", 35: "吉", 37: "吉", 38: "吉",
    43: "吉", 44: "吉", 45: "吉", 46: "吉", 47: "吉",
    53: "吉", 54: "吉", 56: "吉", 58: "吉", 62: "吉",
    65: "吉", 68: "吉", 69: "吉", 71: "吉", 99: "吉",

    # 半吉 (5个)
    9: "半吉", 48: "半吉", 55: "半吉", 63: "半吉", 67: "半吉",

    # 小吉 (4个)
    27: "小吉", 49: "小吉", 60: "小吉", 61: "小吉",

    # 末吉 (3个)
    39: "末吉", 50: "末吉", 70: "末吉",

    # 凶 (30个)
    17: "凶", 18: "凶", 19: "凶", 36: "凶", 40: "凶",
    57: "凶", 59: "凶", 66: "凶", 72: "凶", 73: "凶",
    74: "凶", 75: "凶", 76: "凶", 77: "凶", 78: "凶",
    79: "凶", 80: "凶", 81: "凶", 82: "凶", 83: "凶",
    84: "凶", 85: "凶", 86: "凶", 87: "凶", 88: "凶",
    90: "凶", 91: "凶", 95: "凶", 96: "凶", 98: "凶",

    # 大凶 (6个)
    29: "大凶", 89: "大凶", 92: "大凶", 93: "大凶", 94: "大凶", 97: "大凶",
}

def verify_fortune_levels():
    """验证所有签文的签级是否正确"""

    # 读取JSON数据
    json_file = "omikuji/data/senso-ji-fortunes-full.json"
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    fortunes = data['fortunes']

    print("🔍 验证签文签级与浅草寺官方签级的对应关系")
    print("=" * 60)

    errors = []
    success_count = 0

    # 签级映射（英文到中文）
    level_map = {
        "excellent": "大吉",
        "大吉": "大吉",
        "good": "吉",
        "吉": "吉",
        "half_blessing": "半吉",
        "半吉": "半吉",
        "small_blessing": "小吉",
        "小吉": "小吉",
        "future_blessing": "末吉",
        "末吉": "末吉",
        "bad": "凶",
        "凶": "凶",
        "very_bad": "大凶",
        "大凶": "大凶",
    }

    # 检查每个签
    for fortune in fortunes:
        fortune_id = fortune['id']
        current_level = level_map.get(fortune.get('level', ''), fortune.get('level', '未知'))
        expected_level = SENSO_JI_FORTUNE_LEVELS.get(fortune_id, '未知')

        if current_level != expected_level:
            errors.append({
                'id': fortune_id,
                'current': current_level,
                'expected': expected_level
            })
            print(f"❌ 签号 {fortune_id:3d}: {current_level:4s} → 应为 {expected_level}")
        else:
            success_count += 1

    # 输出结果
    print()
    print("-" * 60)
    print(f"✅ 正确匹配：{success_count} 个签")
    print(f"❌ 签级错误：{len(errors)} 个签")

    if errors:
        print("\n发现以下签级错误：")
        print("-" * 60)
        for err in errors:
            print(f"  第 {err['id']:3d} 签: {err['current']:4s} → 应为 {err['expected']}")

    return errors

def fix_fortune_levels(errors):
    """修复签文签级"""

    if not errors:
        print("\n✅ 无需修复")
        return

    print("\n🔧 开始修复签级...")

    # 签级映射（中文到英文，保持一致性）
    level_reverse_map = {
        "大吉": "大吉",
        "吉": "吉",
        "半吉": "半吉",
        "小吉": "小吉",
        "末吉": "末吉",
        "凶": "凶",
        "大凶": "大凶",
    }

    # 读取JSON数据
    json_file = "omikuji/data/senso-ji-fortunes-full.json"
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 修复每个错误
    for err in errors:
        fortune_id = err['id']
        for fortune in data['fortunes']:
            if fortune['id'] == fortune_id:
                old_level = fortune['level']
                new_level = level_reverse_map.get(err['expected'], err['expected'])
                fortune['level'] = new_level
                print(f"✓ 第 {fortune_id:3d} 签: {old_level} → {new_level}")

    # 保存修复后的数据
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 修复完成！已更新 {json_file}")

if __name__ == "__main__":
    errors = verify_fortune_levels()

    if errors:
        print("\n" + "=" * 60)
        choice = input("\n是否自动修复这些签级错误？(y/N): ").strip().lower()
        if choice == 'y':
            fix_fortune_levels(errors)
            print("\n🎉 修复完成！所有签级已与浅草寺官方对应。")
        else:
            print("\n❌ 已取消修复")
    else:
        print("\n🎉 所有签级完全正确，与浅草寺官方100签对应！")
