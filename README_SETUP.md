# 🎯 快速开始 - 5 步完成部署

## ⚡ 快速设置（推荐）

运行以下命令，自动打开所有需要的页面：

```bash
./quick_setup.sh
```

或者手动访问以下页面：

---

## 📋 完整步骤

### 步骤 1️⃣：配置 GitHub Secrets（必需）

**访问：** https://github.com/Summy-Chen/thinkdeep-ai/settings/secrets/actions

点击 **"New repository secret"**，依次添加以下 6 个 Secrets：

| Secret 名称 | 值 | 获取方式 |
|-----------|-----|---------|
| `GEMINI_API_KEY` | 你的 Google Gemini API Key | https://makersuite.google.com/app/apikey |
| `EMAIL_SENDER` | `chenysh48@foxmail.com` | 你的发件邮箱 |
| `EMAIL_PASSWORD` | `byxjmepqwtnycabc` | 邮箱授权码（不是登录密码） |
| `EMAIL_RECIPIENT` | `chenysh48@foxmail.com` | 收件邮箱 |
| `SMTP_SERVER` | `smtp.qq.com` | SMTP 服务器地址 |
| `SMTP_PORT` | `465` | SMTP 端口号 |

**⚠️ 重要：** 所有 Secrets 必须全部配置，否则工作流会失败！

---

### 步骤 2️⃣：启用 GitHub Pages

**访问：** https://github.com/Summy-Chen/thinkdeep-ai/settings/pages

1. 在 **"Build and deployment"** 部分
2. **Source** 选择：**GitHub Actions**（重要：不是 "Deploy from a branch"）
3. 点击 **"Save"** 保存

---

### 步骤 3️⃣：手动触发工作流（首次测试）

**访问：** https://github.com/Summy-Chen/thinkdeep-ai/actions

1. 点击左侧的 **"AI Daily Digest"** 工作流
2. 点击右侧的 **"Run workflow"** 按钮
3. 选择分支：**main**
4. 点击绿色的 **"Run workflow"** 按钮

---

### 步骤 4️⃣：等待部署完成

1. 在工作流运行页面，点击最新的运行记录
2. 查看每个步骤的状态：
   - ✅ 绿色对勾 = 成功
   - 🟡 黄色圆圈 = 运行中
   - 🔴 红色叉 = 失败（点击查看错误）

**预计时间：** 1-3 分钟

---

### 步骤 5️⃣：访问你的网站

部署成功后，访问：

**🌐 https://summy-chen.github.io/thinkdeep-ai/**

如果显示 404，请等待 5-10 分钟后刷新。GitHub Pages 部署需要一些时间。

---

## ✅ 验证清单

完成以下所有步骤后，你的网站应该可以正常访问：

- [ ] ✅ 所有 6 个 GitHub Secrets 已配置
- [ ] ✅ GitHub Pages 已启用（Source = GitHub Actions）
- [ ] ✅ 工作流已手动触发
- [ ] ✅ 所有步骤显示绿色对勾
- [ ] ✅ 网站可以正常访问
- [ ] ✅ 网页显示最新的 AI 资讯

---

## 🔄 自动化运行

配置完成后，工作流会：
- **每天自动运行**：UTC 00:00（北京时间 08:00）
- **自动抓取**：最新的 AI 领域资讯
- **自动生成**：data.json 文件
- **自动部署**：更新网站内容

你也可以随时在 Actions 页面手动触发工作流来更新内容。

---

## 🆘 遇到问题？

### 常见问题快速解决：

1. **工作流失败** → 检查 Secrets 是否全部配置
2. **构建失败** → 查看工作流日志中的错误信息
3. **网页 404** → 等待 5-10 分钟后刷新
4. **data.json 不存在** → 检查 GEMINI_API_KEY 是否正确

**详细故障排查：** 查看 `SETUP_COMPLETE.md` 文件

---

## 📚 相关文档

- `SETUP_COMPLETE.md` - 完整设置指南（详细版）
- `CHECKLIST.md` - 检查清单
- `DEPLOY_GUIDE.md` - 原始部署指南

---

**需要帮助？** 查看工作流运行日志或参考详细文档。

