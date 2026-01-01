# ThinkDeep.ai - GitHub 零成本部署指南

本指南将帮助您将 ThinkDeep.ai 部署到 GitHub，实现每日自动抓取、生成简报并更新网页。

## 1. 准备工作

1.  注册一个 [GitHub 账号](https://github.com/)（如果您还没有）。
2.  下载本压缩包中的所有文件。

## 2. 创建 GitHub 仓库

1.  登录 GitHub，点击右上角的 **+** 号，选择 **New repository**。
2.  Repository name 填写 `thinkdeep-ai`（或其他您喜欢的名字）。
3.  选择 **Public**（公开仓库，免费使用 Actions）。
4.  点击 **Create repository**。

## 3. 上传代码

1.  在您的电脑上，将下载的 `github_deploy` 文件夹中的内容（包括 `.github` 文件夹）上传到刚才创建的仓库。
    *   **推荐方式**：使用 GitHub Desktop 或 Git 命令行工具。
    *   **简单方式**：在仓库页面点击 "uploading an existing file"，直接拖入所有文件（注意保持目录结构）。

## 4. 配置 Secrets (关键步骤)

为了保护您的 API Key 和邮箱密码，我们需要在 GitHub Secrets 中配置它们。

1.  进入仓库页面，点击 **Settings** -> **Secrets and variables** -> **Actions**。
2.  点击 **New repository secret**，依次添加以下变量：

| Name | Value (填入您的具体信息) |
| :--- | :--- |
| `GEMINI_API_KEY` | 您的 Google Gemini API Key |
| `EMAIL_SENDER` | `chenysh48@foxmail.com` |
| `EMAIL_PASSWORD` | `byxjmepqwtnycabc` |
| `EMAIL_RECIPIENT` | `chenysh48@foxmail.com` |
| `SMTP_SERVER` | `smtp.qq.com` |
| `SMTP_PORT` | `465` |

## 5. 开启 GitHub Pages

1.  进入仓库页面，点击 **Settings** -> **Pages**。
2.  在 **Build and deployment** 下的 **Source** 选择 **GitHub Actions**。
3.  这就完成了！GitHub 会自动根据我们的配置（`.github/workflows/daily_digest.yml`）来部署网页。

## 6. 验证运行

1.  点击仓库上方的 **Actions** 标签页。
2.  您应该能看到一个名为 "AI Daily Digest" 的工作流。
3.  如果它没有自动运行，您可以点击左侧的 "AI Daily Digest"，然后点击右侧的 **Run workflow** 手动触发一次。
4.  运行成功后（显示绿色对勾），您的网页就会上线！
    *   访问地址通常是：`https://您的用户名.github.io/thinkdeep-ai/`

## 常见问题

*   **邮件没收到？** 请检查垃圾邮件箱，或者确认 Secrets 中的密码是否正确。
*   **网页没更新？** 请查看 Actions 的运行日志，确认是否有抓取错误。
*   **想修改配置？** 直接修改仓库中的 `backend/config.py` 文件即可。

---
© 2025 ThinkDeep.ai
