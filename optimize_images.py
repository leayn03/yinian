#!/usr/bin/env python3
"""
图片优化脚本 - 压缩签文图片以减少部署大小
使用 Pillow 库将图片质量降低到 85%，可减少约 30-40% 的文件大小
"""

import os
from PIL import Image
from pathlib import Path

def optimize_images(input_dir, output_dir=None, quality=85):
    """
    优化图片大小

    Args:
        input_dir: 输入目录路径
        output_dir: 输出目录路径（如果为None，则覆盖原文件）
        quality: JPEG 质量（1-100，推荐 80-90）
    """
    if output_dir is None:
        output_dir = input_dir

    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    total_original = 0
    total_optimized = 0
    count = 0

    print(f"🖼️  开始优化图片...")
    print(f"📁 输入目录: {input_path}")
    print(f"📂 输出目录: {output_path}")
    print(f"⚙️  JPEG 质量: {quality}%")
    print("-" * 50)

    for img_file in input_path.glob("*.jpg"):
        try:
            # 打开图片
            img = Image.open(img_file)

            # 原始大小
            original_size = img_file.stat().st_size

            # 输出路径
            output_file = output_path / img_file.name

            # 优化并保存
            img.save(
                output_file,
                "JPEG",
                quality=quality,
                optimize=True,
                progressive=True  # 渐进式 JPEG
            )

            # 优化后大小
            optimized_size = output_file.stat().st_size

            # 统计
            total_original += original_size
            total_optimized += optimized_size
            count += 1

            reduction = (1 - optimized_size / original_size) * 100

            print(f"✓ {img_file.name}: {original_size/1024:.1f}KB → {optimized_size/1024:.1f}KB (-{reduction:.1f}%)")

        except Exception as e:
            print(f"✗ {img_file.name}: 错误 - {e}")

    print("-" * 50)
    print(f"✅ 完成！优化了 {count} 张图片")
    print(f"📊 原始总大小: {total_original/1024/1024:.2f} MB")
    print(f"📊 优化后大小: {total_optimized/1024/1024:.2f} MB")
    print(f"💾 节省空间: {(total_original-total_optimized)/1024/1024:.2f} MB ({(1-total_optimized/total_original)*100:.1f}%)")

if __name__ == "__main__":
    import sys

    # 检查是否安装了 Pillow
    try:
        from PIL import Image
    except ImportError:
        print("❌ 错误：未安装 Pillow 库")
        print("请运行: pip3 install Pillow")
        sys.exit(1)

    # 图片目录
    images_dir = "omikuji/data/senso-ji-omikuji-main"

    if not os.path.exists(images_dir):
        print(f"❌ 错误：目录不存在 - {images_dir}")
        sys.exit(1)

    # 询问是否要优化
    print("🎯 图片优化工具")
    print(f"将优化目录: {images_dir}")
    print("⚠️  警告：此操作会覆盖原始图片！")
    print()

    choice = input("是否继续？(y/N): ").strip().lower()

    if choice == 'y':
        # 推荐质量设置
        print("\n推荐质量设置:")
        print("  85 - 高质量（推荐，减少 30-40%）")
        print("  80 - 中等质量（减少 40-50%）")
        print("  75 - 较低质量（减少 50-60%）")

        quality_input = input("\n选择质量 (1-100, 默认 85): ").strip()
        quality = int(quality_input) if quality_input else 85

        if 1 <= quality <= 100:
            optimize_images(images_dir, quality=quality)
        else:
            print("❌ 无效的质量值，必须在 1-100 之间")
    else:
        print("❌ 已取消")
