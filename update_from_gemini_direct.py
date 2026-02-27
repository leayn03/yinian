#!/usr/bin/env python3
"""
从修正后的senso-gemini.txt更新full.json
使用正则表达式逐个提取签对象
"""

import json
import re

SOURCE_FILE = "omikuji/data/senso-gemini.txt"
TARGET_FILE = "omikuji/data/senso-ji-fortunes-full.json"


def extract_fortunes_from_text(content):
    """使用正则表达式提取所有签对象"""

    # 预处理：移除所有特殊标记
    content = content.replace('[cite_start]', '')
    content = re.sub(r'\[cite:\s*\d+\]', '', content)

    # 逐个提取签对象
    # 模式：从 { "id": xxx 开始到对应的 }
    pattern = r'\{\s*"id"\s*:\s*(\d+)\s*,[^}]*"interpretation"\s*:\s*\{[^}]*\}\s*\}\s*,'

    fortunes = []

    # 使用更简单的方法：找到每个 { "id": X } 块
    # 先分割成单独的对象
    in_object = False
    brace_count = 0
    current_obj = ""
    id_pattern = re.compile(r'"id"\s*:\s*(\d+)')

    for char in content:
        if char == '{' and not in_object:
            in_object = True
            brace_count = 1
            current_obj = char
        elif in_object:
            current_obj += char
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    # 完成一个对象
                    # 检查是否包含id
                    if id_pattern.search(current_obj):
                        try:
                            obj = json.loads(current_obj)
                            fortunes.append(obj)
                        except:
                            pass
                    in_object = False
                    current_obj = ""

    print(f"通过正则提取了 {len(fortunes)} 个签")

    # 按id排序
    fortunes.sort(key=lambda x: x['id'])

    return fortunes


def update_from_gemini():
    """从修正后的gemini数据更新full.json"""

    print("=" * 80)
    print("从修正后的senso-gemini.txt更新full.json")
    print("=" * 80)
    print()

    # 读取修正后的gemini数据
    print(f"读取源文件: {SOURCE_FILE}")
    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    source_data = extract_fortunes_from_text(content)

    if len(source_data) < 100:
        print(f"⚠️  只提取到 {len(source_data)} 个签，尝试继续...")
        # 继续处理

    print()

    # 创建签号到签文的映射
    fortune_map = {}
    for item in source_data:
        fortune_map[item['id']] = item

    # 读取目标full.json
    print(f"读取目标文件: {TARGET_FILE}")
    with open(TARGET_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"  - 目标文件包含 {len(data['fortunes'])} 个签")
    print()

    # 更新每个签的数据
    print("开始更新数据...")
    updated_count = 0
    poem_changes = []

    for fortune in data['fortunes']:
        fortune_id = fortune['id']

        if fortune_id in fortune_map:
            source_item = fortune_map[fortune_id]

            old_poem = fortune['poem']['lines']
            new_poem = source_item['poem']['lines']

            if old_poem != new_poem:
                poem_changes.append((fortune_id, old_poem, new_poem))

            # 更新签级
            fortune['level'] = source_item['level']

            # 更新签诗
            fortune['poem'] = {
                'title': source_item['poem']['title'],
                'lines': source_item['poem']['lines'],
                'source': '浅草寺',
                'lineInterpretations': source_item['poem'].get('lineInterpretations', [])
            }

            # 更新解释
            interp = source_item['interpretation']
            fortune['interpretation'] = {
                'summary': interp.get('summary', ''),
                'career': interp.get('career', ''),
                'love': interp.get('love', ''),
                'health': interp.get('health', ''),
                'advice': interp.get('advice', ''),
                'story': interp.get('story', '')
            }

            updated_count += 1

    # 保存更新后的数据
    print(f"  - 成功更新 {updated_count} 个签")
    print()

    with open(TARGET_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # 显示诗句变更（前3个）
    if poem_changes:
        print("诗句变更（前3个）：")
        print("-" * 60)
        for fid, old, new in poem_changes[:3]:
            print(f"  第 {fid} 签:")
            print(f"    原文: {' | '.join(old)}")
            print(f"    新文: {' | '.join(new)}")
            print()

    # 统计新的签级分布
    level_count = {}
    for fortune in data['fortunes']:
        level = fortune['level']
        level_count[level] = level_count.get(level, 0) + 1

    print("新的签级分布：")
    print("-" * 40)
    for level, count in sorted(level_count.items(), key=lambda x: -x[1]):
        print(f"  {level}: {count} 个")
    print()

    print("=" * 80)
    print("✅ 更新完成！")
    print("=" * 80)


if __name__ == "__main__":
    update_from_gemini()
