#!/bin/bash

# 一念 - 快速启动脚本

echo "🎲 一念 - 浅草寺御神签"
echo "━━━━━━━━━━━━━━━━━━━━"
echo ""

# 检查是否在正确的目录
if [ ! -d "omikuji" ]; then
    echo "❌ 错误：未找到 omikuji 目录"
    echo "请在项目根目录运行此脚本"
    exit 1
fi

# 进入项目目录
cd omikuji

echo "📂 当前目录：$(pwd)"
echo ""

# 获取本机IP
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || echo "未获取到IP")
else
    # Linux
    LOCAL_IP=$(hostname -I | awk '{print $1}')
fi

echo "🌐 启动本地服务器..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━"
echo "✅ 服务器已启动！"
echo ""
echo "📱 访问地址："
echo "  电脑浏览器：http://localhost:8080"
if [ "$LOCAL_IP" != "未获取到IP" ]; then
    echo "  手机浏览器：http://$LOCAL_IP:8080"
fi
echo ""
echo "💡 提示："
echo "  • 电脑上点击【点击模拟摇动】抽签"
echo "  • 手机上摇动手机抽签"
echo "  • iOS使用Safari，首次需允许传感器权限"
echo "  • 按 Ctrl+C 停止服务器"
echo "━━━━━━━━━━━━━━━━━━━━"
echo ""

# 启动Python HTTP服务器
python3 -m http.server 8080
