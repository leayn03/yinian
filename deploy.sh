#!/bin/bash

# 一念 - Vercel 快速部署脚本

echo "🚀 一念 - Vercel 部署助手"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 检查是否安装了 vercel CLI
if ! command -v vercel &> /dev/null; then
    echo "❌ 未检测到 Vercel CLI"
    echo ""
    echo "请先安装 Vercel CLI："
    echo "  npm install -g vercel"
    echo ""
    echo "或使用 Web 界面部署（参考 DEPLOY.md）"
    exit 1
fi

echo "✅ Vercel CLI 已安装"
echo ""

# 询问是否要优化图片
echo "📦 部署前准备"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "图片优化（可选）："
echo "  • 当前图片大小：~38MB"
echo "  • 优化后大小：~22-26MB（减少 30-40%）"
echo "  • 需要安装 Pillow：pip3 install Pillow"
echo ""

read -p "是否运行图片优化？(y/N): " optimize_choice

if [[ "$optimize_choice" == "y" || "$optimize_choice" == "Y" ]]; then
    if command -v python3 &> /dev/null; then
        if python3 -c "import PIL" 2>/dev/null; then
            echo ""
            echo "🖼️  开始优化图片..."
            python3 optimize_images.py
        else
            echo ""
            echo "⚠️  未安装 Pillow 库"
            echo "请运行: pip3 install Pillow"
            echo ""
            read -p "跳过优化继续部署？(Y/n): " continue_choice
            if [[ "$continue_choice" == "n" || "$continue_choice" == "N" ]]; then
                exit 1
            fi
        fi
    else
        echo "❌ 未找到 Python 3"
        exit 1
    fi
else
    echo "⏭️  跳过图片优化"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 部署选项
echo "🌐 部署选项："
echo "  1) 预览部署（开发环境）"
echo "  2) 生产部署（正式环境）"
echo ""

read -p "请选择 (1/2): " deploy_choice

case $deploy_choice in
    1)
        echo ""
        echo "🔨 开始预览部署..."
        vercel
        ;;
    2)
        echo ""
        echo "🚀 开始生产部署..."
        vercel --prod
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 部署完成！"
echo ""
echo "📱 下一步："
echo "  1. 在浏览器中打开部署链接"
echo "  2. 测试所有功能（抽签、图片、历史记录）"
echo "  3. 手机上测试摇一摇功能"
echo "  4. 查看 DEPLOY.md 了解更多配置"
echo ""
echo "愿每次抽签都带来好运！🎲✨"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
