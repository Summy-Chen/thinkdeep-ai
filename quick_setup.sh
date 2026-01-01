#!/bin/bash

# ThinkDeep.ai 快速设置脚本
# 此脚本会打开所有必要的 GitHub 页面

echo "🚀 ThinkDeep.ai 部署设置助手"
echo "================================"
echo ""

# 打开 Secrets 配置页面
echo "📝 步骤 1: 配置 GitHub Secrets"
echo "正在打开 Secrets 配置页面..."
open "https://github.com/Summy-Chen/thinkdeep-ai/settings/secrets/actions"
sleep 2

# 打开 Pages 设置页面
echo "📄 步骤 2: 配置 GitHub Pages"
echo "正在打开 Pages 设置页面..."
open "https://github.com/Summy-Chen/thinkdeep-ai/settings/pages"
sleep 2

# 打开 Actions 页面
echo "⚙️  步骤 3: 触发工作流"
echo "正在打开 Actions 页面..."
open "https://github.com/Summy-Chen/thinkdeep-ai/actions"
sleep 2

echo ""
echo "✅ 所有页面已打开！"
echo ""
echo "📋 接下来请按照以下步骤操作："
echo ""
echo "1️⃣  在 Secrets 页面，添加以下 6 个 Secrets："
echo "   - GEMINI_API_KEY"
echo "   - EMAIL_SENDER"
echo "   - EMAIL_PASSWORD"
echo "   - EMAIL_RECIPIENT"
echo "   - SMTP_SERVER"
echo "   - SMTP_PORT"
echo ""
echo "2️⃣  在 Pages 页面，设置 Source 为 'GitHub Actions'"
echo ""
echo "3️⃣  在 Actions 页面，点击 'Run workflow' 手动触发"
echo ""
echo "4️⃣  等待部署完成（约 1-3 分钟）"
echo ""
echo "5️⃣  访问网站：https://summy-chen.github.io/thinkdeep-ai/"
echo ""
echo "📖 详细说明请查看 SETUP_COMPLETE.md 文件"
echo ""

