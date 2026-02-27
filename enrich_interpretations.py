#!/usr/bin/env python3
"""
根据签诗和逐句解释丰富现代释义
"""

import json

DATA_FILE = "omikuji/data/senso-ji-fortunes-full.json"


def generate_interpretation(fortune):
    """根据签诗生成更丰富的释义"""

    level = fortune['level']
    poem_lines = fortune['poem']['lines']
    line_interp = fortune['poem'].get('lineInterpretations', [])
    existing = fortune['interpretation']

    # 主题提取（从诗句中关键词）
    all_text = ''.join(poem_lines)
    sentiment = 'positive'
    if level in ['凶', '末小吉']:
        sentiment = 'negative'
    elif any(kw in all_text for kw in ['愁', '损', '失', '阻', '忧']):
        sentiment = 'cautious'

    # 完全重新生成所有释义
    summary = generate_summary(level, poem_lines, line_interp, sentiment)
    career = generate_career(level, poem_lines, sentiment)
    love = generate_love(level, poem_lines, sentiment)
    health = generate_health(level, poem_lines, sentiment)
    advice = generate_advice(level, poem_lines, sentiment)
    story = generate_story(level, poem_lines, line_interp)

    return {
        'summary': summary,
        'career': career,
        'love': love,
        'health': health,
        'advice': advice,
        'story': story
    }


def generate_summary(level, poem_lines, line_interp, sentiment):
    """生成总体运势"""
    templates = {
        '大吉': [
            "此签大吉。运势如日中天，所求皆顺。{theme}，宜积极进取把握良机。",
            "此签上上大吉。天时地利人和齐聚，{theme}，正当其时大展宏图。",
            "大吉之兆。祥瑞降临，{theme}，诸事顺遂，功成名就可期。"
        ],
        '吉': [
            "此签为吉。运势良好，{theme}，稳步向前必有所获。",
            "吉兆。时机渐熟，{theme}，保持专注向好而行。",
            "吉签。顺中有进，{theme}，持之以恒可见成果。"
        ],
        '末吉': [
            "此签末吉。初始平缓，{theme}，耐心等待后福可期。",
            "末吉之兆。先难后易，{theme}，积蓄力量待时而动。"
        ],
        '小吉': [
            "此签小吉。平稳向好，{theme}，小步积累渐进改善。",
            "小吉之兆。微福渐至，{theme}，稳扎稳打自有收获。"
        ],
        '半吉': [
            "此签半吉。吉凶参半，{theme}，需谨慎权衡步步为营。",
            "半吉之兆。喜忧并存，{theme}，宜静观其变灵活应对。"
        ],
        '末小吉': [
            "此签末小吉。转吉之前，{theme}，坚守本分静待转机。",
            "末小吉之兆。黎明前暗，{theme}，韬光养晦等待时机。"
        ],
        '凶': [
            "此签为凶。运势欠佳，{theme}，宜守不宜动多作检讨。",
            "凶兆。阻碍重重，{theme}，低调行事修身养性。",
            "凶签。前路多艰，{theme}，耐心等待雨过天晴。"
        ]
    }

    theme = extract_theme(poem_lines)
    template = templates.get(level, templates['吉'])[0]

    return template.format(theme=theme)


def generate_career(level, poem_lines, sentiment):
    """生成事业财运"""
    if level == '大吉':
        return "事业运势旺盛，贵人相助，升职加薪机会降临。财运亨通，投资理财皆有利可图。把握当前良机，大胆施展抱负。"
    elif level == '吉':
        return "事业稳步发展，工作顺利获得认可。财运平稳，正财稳定，可适度理财。保持专注，持续努力必有回报。"
    elif level in ['末吉', '小吉']:
        return "事业平稳向好，小有进展。财运平平，收支平衡，宜稳中求进。耐心积累，渐进改善。"
    elif level == '半吉':
        return "事业喜忧参半，需谨慎决策。财运起伏，避免冒险投资，稳守为上。"
    elif level == '末小吉':
        return "事业处于低潮期，宜保持低调。财运不佳，避免重大开支，静待转机。"
    else:  # 凶
        return "事业运势低迷，阻碍较多，宜稳守现状。财运不佳，避免投资投机，谨慎理财。修身养性等待时机好转。"


def generate_love(level, poem_lines, sentiment):
    """生成感情姻缘"""
    if level == '大吉':
        return "感情运极佳，单身者桃花旺，有望遇见良缘。有伴侣者感情升温，关系更近一步，婚嫁事宜顺遂。"
    elif level == '吉':
        return "感情运势良好，单身者有机会认识心仪对象。有伴侣者相处和睦，关系稳定发展。"
    elif level in ['末吉', '小吉']:
        return "感情平稳渐进，单身者不必强求，缘分自然来。有伴侣者维持现状，细水长流。"
    elif level == '半吉':
        return "感情运势起伏，需多沟通理解。避免冲动决定，给彼此一些空间。"
    elif level == '末小吉':
        return "感情处于平淡期，不宜急于求成。单身者耐心等待，有伴侣者多包容体谅。"
    else:  # 凶
        return "感情运势低迷，易生误会争执。单身者暂缓追求，有伴侣者需冷静处理问题，多沟通少指责。"


def generate_health(level, poem_lines, sentiment):
    """生成健康平安"""
    if level in ['大吉', '吉']:
        return "身体状况良好，精神饱满。保持规律作息和适度运动，健康运势佳。"
    elif level in ['末吉', '小吉']:
        return "健康状况平稳，注意劳逸结合。适度休息，避免过度劳累。"
    elif level == '半吉':
        return "健康运势一般，注意小病小痛。保持良好作息，饮食清淡。"
    else:  # 凶, 末小吉
        return "健康运势欠佳，注意身体保养。避免过度劳累，保持心情愉悦，定期检查。"


def generate_advice(level, poem_lines, sentiment):
    """生成建议"""
    if level in ['大吉', '吉']:
        return "把握当下好运，积极进取。保持谦逊态度，广结善缘，为未来持续积累福气。"
    elif level in ['末吉', '小吉']:
        return "稳步前行，不急不躁。积累经验和资源，为更好的机会做准备。"
    elif level == '半吉':
        return "谨慎决策，权衡利弊。保持冷静，灵活应对变化，稳中求进。"
    else:  # 凶, 末小吉
        return "低调行事，韬光养晦。修身养性，反思总结，等待运势好转再行动。"


def generate_story(level, poem_lines, line_interp):
    """生成典故说明"""
    # 基于诗句意境生成
    if line_interp and len(line_interp) > 0:
        main_theme = line_interp[0] if line_interp else ""
    else:
        main_theme = poem_lines[0] if poem_lines else ""

    return f"此签诗意取自「{poem_lines[0][:4]}...」，寓意{main_theme[:30]}。古人以诗喻理，揭示人生起伏变迁之理。"


def extract_theme(poem_lines):
    """从诗句中提取主题"""
    theme_map = {
        '云': '云开雾散，前景光明',
        '月': '明月当空，清辉普照',
        '花': '花开富贵，事业兴旺',
        '春': '枯木逢春，否极泰来',
        '山': '高山仰止，步步高升',
        '水': '顺风顺水，一帆风顺',
        '风': '风生水起，运势亨通',
        '宝': '珍宝现世，福缘深厚',
        '塔': '七级浮屠，功德圆满',
        '龙': '龙腾云起，飞黄腾达',
        '舟': '扬帆起航，前程远大'
    }

    for keyword, theme in theme_map.items():
        if any(keyword in line for line in poem_lines):
            return theme

    # 默认主题
    return "运势通达"


def main():
    print("=" * 80)
    print("丰富签文释义内容")
    print("=" * 80)
    print()

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"处理 {len(data['fortunes'])} 个签...")
    print()

    updated = 0
    for fortune in data['fortunes']:
        # 完全重新生成所有释义
        new_interp = generate_interpretation(fortune)
        fortune['interpretation'] = new_interp
        updated += 1

        if updated <= 5:  # 显示前5个示例
            print(f"第 {fortune['id']} 签 ({fortune['level']}):")
            print(f"  summary: {new_interp['summary']}")
            print(f"  career: {new_interp['career'][:50]}...")
            print()

    print(f"共更新 {updated} 个签的释义")
    print()

    # 保存
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("=" * 80)
    print("✅ 更新完成！")
    print("=" * 80)


if __name__ == "__main__":
    main()
