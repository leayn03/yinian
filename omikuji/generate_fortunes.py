#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成浅草寺100条签文数据
基于senso-ji-omikuji-main文件夹中的图片
"""

import json
import os

# 签级映射（根据浅草寺实际分布）
LEVEL_MAPPING = {
    # 大吉 (17条): 1, 2, 3, 5, 7, 14, 20, 24, 26, 28, 32, 54, 56, 63, 78, 80, 94
    "excellent": [1, 2, 3, 5, 7, 14, 20, 24, 26, 28, 32, 54, 56, 63, 78, 80, 94],

    # 吉 (35条): 4, 6, 10, 11, 13, 16, 18, 19, 21, 23, 25, 27, 31, 33, 35, 37, 40, 42, 44, 46, 48, 50, 52, 55, 57, 60, 62, 64, 66, 68, 72, 74, 76, 82, 84
    "good": [4, 6, 10, 11, 13, 16, 18, 19, 21, 23, 25, 27, 31, 33, 35, 37, 40, 42, 44, 46, 48, 50, 52, 55, 57, 60, 62, 64, 66, 68, 72, 74, 76, 82, 84],

    # 半吉 (5条): 8, 30, 38, 49, 67
    "medium": [8, 30, 38, 49, 67],

    # 小吉 (4条): 12, 41, 51, 85
    "small": [12, 41, 51, 85],

    # 末吉 (3条): 9, 22, 53
    "末吉": [9, 22, 53],

    # 凶 (30条): 15, 17, 34, 36, 39, 43, 45, 47, 58, 59, 61, 65, 69, 70, 71, 73, 75, 77, 79, 81, 83, 86, 87, 88, 89, 90, 91, 92, 96, 98
    "poor": [15, 17, 34, 36, 39, 43, 45, 47, 58, 59, 61, 65, 69, 70, 71, 73, 75, 77, 79, 81, 83, 86, 87, 88, 89, 90, 91, 92, 96, 98],

    # 大凶 (6条): 29, 93, 95, 97, 99, 100
    "worst": [29, 93, 95, 97, 99, 100]
}

# 反向映射
NUMBER_TO_LEVEL = {}
for level, numbers in LEVEL_MAPPING.items():
    for num in numbers:
        NUMBER_TO_LEVEL[num] = level

# 签级中文名
LEVEL_CHINESE = {
    "excellent": "大吉",
    "good": "吉",
    "medium": "半吉",
    "small": "小吉",
    "末吉": "末吉",
    "poor": "凶",
    "worst": "大凶"
}

# 示例签诗和解读模板
FORTUNE_TEMPLATES = {
    "excellent": {
        "summary": "此签大吉。运势极佳，诸事顺遂，如日中天。把握机会，积极进取，必有所成。",
        "career": "事业运势旺盛，工作顺利，可能获得晋升或重要机会。领导赏识，同事支持，是展现才华的最佳时机。",
        "love": "感情运势极佳。单身者桃花运旺，易遇良缘；有伴者感情稳固，可能迈入新阶段。真诚相待，幸福美满。",
        "health": "身心健康，精力充沛。适合开始新的健身计划，效果显著。保持良好作息，健康会持续提升。",
        "advice": "机遇难得，把握当下。勇敢追求目标，但也要谦虚谨慎。广结善缘，福泽绵长。"
    },
    "good": {
        "summary": "此签为吉。运势良好，诸事平稳向好。只要踏实努力，定能收获成果。",
        "career": "工作运势稳定，会有新的机会出现。把握时机，主动展现能力。稳扎稳打，循序渐进。",
        "love": "感情运势平稳。单身者可能遇到心仪对象；有伴者感情和谐。自然发展，水到渠成。",
        "health": "整体健康状况良好，精力尚可。注意日常保养，适当运动，健康会持续保持。",
        "advice": "保持乐观心态，积极面对生活。好运需要主动把握，脚踏实地，稳步前进。"
    },
    "medium": {
        "summary": "此签半吉半凶。运势平平，需要谨慎。有机遇也有挑战，保持警惕，稳中求进。",
        "career": "工作总体尚可，但要注意防范问题。不要过于张扬，低调做事。重要决策要多方考虑。",
        "love": "感情平稳但需要用心维护。避免第三者介入，多沟通增进感情。不宜冒进。",
        "health": "健康需要注意，小心意外。避免危险活动，注意安全。适度休息，调养身心。",
        "advice": "谨慎行事，防患于未然。不要轻信他人，重要事情要亲自确认。稳守为宜。"
    },
    "small": {
        "summary": "此签为小吉。运势小有起色，但不宜期望过高。脚踏实地，积少成多。",
        "career": "工作有小进展，但不明显。继续努力，不要气馁。小步前进，积累经验。",
        "love": "感情有小进步，但需要耐心。单身者不宜着急；有伴者慢慢培养感情。",
        "health": "健康状况一般，注意调养。避免过度劳累，保持规律作息。",
        "advice": "知足常乐，不要贪多。珍惜眼前，脚踏实地。小成功也值得庆祝。"
    },
    "末吉": {
        "summary": "此签为末吉。运势平淡，无大喜大悲。守住本分，平安即是福。",
        "career": "工作波澜不惊，维持现状。不宜大变动，稳守岗位。充实自己，等待时机。",
        "love": "感情平淡如水，但也稳定。单身者缘分未到；有伴者平平淡淡才是真。",
        "health": "健康无大碍，维持现状。注意日常保健，预防为主。",
        "advice": "平淡是福，安稳是金。不要强求，顺其自然。保持平常心，静待转机。"
    },
    "poor": {
        "summary": "此签为凶。运势不佳，诸事不顺。宜守不宜攻，谨慎行事，避免损失。",
        "career": "工作遇到阻碍，进展不顺。可能遭遇困难或挫折。此时不宜大动作，稳守为上。",
        "love": "感情运势低迷，可能有误会或争执。不要做重大决定。冷静处理，避免冲动。",
        "health": "健康需要注意，特别是安全问题。避免冒险，注意休息调养。",
        "advice": "时运不济，宜守不宜攻。减少外出，避免冒险。等待时机，韬光养晦。"
    },
    "worst": {
        "summary": "此签为大凶。运势极差，困境重重。需要接受现实，及时止损，等待转机。",
        "career": "事业陷入困境，处处受限。可能遭遇重大挫折。不要勉强，及时止损。反思问题，等待时机。",
        "love": "感情面临危机，可能分手或破裂。强求无益，不如放手。单身者不宜追求新恋情。",
        "health": "健康状况堪忧，需要重视。及时就医，配合治疗。心理压力大，寻求专业帮助。",
        "advice": "困境难以立即解决，接受现实很重要。不要强求，学会放下执念。困境也是成长的机会。"
    }
}

def generate_fortune_data(number):
    """生成单条签文数据"""
    level = NUMBER_TO_LEVEL.get(number, "good")
    level_chinese = LEVEL_CHINESE.get(level, "吉")
    template = FORTUNE_TEMPLATES.get(level, FORTUNE_TEMPLATES["good"])

    fortune = {
        "id": number,
        "level": level,
        "imageFront": f"senso-ji-omikuji-main/{number}_0.jpg",
        "imageBack": f"senso-ji-omikuji-main/{number}_1.jpg",
        "poem": {
            "title": f"第{number}签",
            "lines": [
                f"签文第{number}首",
                "详细内容请查看图片",
                "日文原文准确",
                "现代解读如下"
            ],
            "source": "浅草寺"
        },
        "interpretation": {
            "summary": template["summary"],
            "career": template["career"],
            "love": template["love"],
            "health": template["health"],
            "advice": template["advice"],
            "story": f"此为浅草寺第{number}签，签级为{level_chinese}。详细签文请查看签文图片。"
        }
    }

    return fortune

def main():
    """生成完整的100条签文数据"""
    fortunes = []

    # 生成100条签文
    for i in range(1, 101):
        fortune = generate_fortune_data(i)
        fortunes.append(fortune)

    # 统计签级分布
    distribution = {}
    for fortune in fortunes:
        level = LEVEL_CHINESE.get(fortune["level"], "未知")
        distribution[level] = distribution.get(level, 0) + 1

    # 创建完整数据结构
    data = {
        "metadata": {
            "version": "1.0",
            "source": "浅草寺御神签（Senso-ji Omikuji）",
            "totalCount": 100,
            "description": "日本东京浅草寺传统御神签，包含大吉、吉、半吉、小吉、末吉、凶、大凶等签级",
            "lastUpdated": "2026-02-27",
            "distribution": distribution,
            "note": "签文详细内容请查看对应的图片文件，本数据提供现代中文解读"
        },
        "fortunes": fortunes
    }

    # 保存为JSON文件
    output_file = "YiNian-H5/data/senso-ji-fortunes-full.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ 已生成100条签文数据，保存到: {output_file}")
    print(f"\n📊 签级分布:")
    for level, count in sorted(distribution.items()):
        percentage = count / 100 * 100
        print(f"  {level}: {count}条 ({percentage:.1f}%)")

if __name__ == "__main__":
    main()
