# 🚀 Vercel 部署指南

## 📋 部署前准备

### 1. 已完成的优化

✅ **配置文件已创建**
- `vercel.json` - Vercel 部署配置
- `package.json` - 项目描述文件
- `.vercelignore` - 忽略不需要部署的文件

✅ **缓存策略**
- 静态资源（图片、CSS、JS）设置 1 年缓存
- 自动启用 CDN 加速

### 2. 可选优化（推荐）

#### 图片压缩（可减少 30-40% 大小）

```bash
# 安装 Pillow 库
pip3 install Pillow

# 运行优化脚本
python3 optimize_images.py
```

**注意**：此操作会覆盖原始图片，建议先备份！

压缩前：~38MB (202张图片)
压缩后：~22-26MB (质量 85%)

---

## 🌐 部署到 Vercel

### 方法一：通过 Vercel CLI（推荐）

#### 1. 安装 Vercel CLI

```bash
npm install -g vercel
```

#### 2. 登录 Vercel

```bash
vercel login
```

#### 3. 部署项目

```bash
# 在项目根目录运行
cd /Users/leayn/Documents/PythonProject/yinian
vercel
```

首次部署会询问：
- Setup and deploy? → **Y**
- Which scope? → 选择你的账号
- Link to existing project? → **N**
- Project name? → `yinian-omikuji` (或自定义)
- In which directory is your code located? → `./` (直接回车)

#### 4. 生产环境部署

```bash
vercel --prod
```

---

### 方法二：通过 Vercel Web 界面

#### 1. 初始化 Git 仓库（如果还没有）

```bash
cd /Users/leayn/Documents/PythonProject/yinian
git init
git add .
git commit -m "Initial commit: 一念 - 浅草寺御神签应用"
```

#### 2. 推送到 GitHub

```bash
# 创建 GitHub 仓库后
git remote add origin https://github.com/你的用户名/yinian-omikuji.git
git branch -M main
git push -u origin main
```

#### 3. 在 Vercel 导入项目

1. 访问 [vercel.com](https://vercel.com)
2. 点击 "Add New" → "Project"
3. 选择 GitHub 仓库
4. 配置项目：
   - **Framework Preset**: Other
   - **Root Directory**: `./` (保持默认)
   - **Build Command**: (留空)
   - **Output Directory**: (留空)
5. 点击 "Deploy"

---

## ⚙️ 部署配置说明

### vercel.json 配置

```json
{
  "rewrites": [
    // 将根路径重定向到 omikuji 目录
    { "source": "/(.*)", "destination": "/omikuji/$1" }
  ],
  "headers": [
    // 静态资源缓存 1 年
    {
      "source": "/omikuji/data/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

### 路径映射

- 访问 `https://你的域名.vercel.app/` → 实际访问 `/omikuji/index.html`
- 访问 `https://你的域名.vercel.app/css/styles.css` → 实际访问 `/omikuji/css/styles.css`

---

## 📊 部署后检查清单

### 功能测试

- [ ] 首页正常加载
- [ ] 摇一摇功能工作（手机）
- [ ] 点击抽签功能工作（桌面）
- [ ] 签文图片正常显示（正反面）
- [ ] 历史记录保存正常
- [ ] 设置功能正常
- [ ] 页面转场动画流畅

### 性能测试

- [ ] 首屏加载时间 < 3秒
- [ ] 图片加载正常（检查 Network 标签）
- [ ] 移动端体验流畅
- [ ] 检查 Lighthouse 分数（目标：>90）

### SEO 优化（可选）

在 `omikuji/index.html` 中添加：

```html
<meta name="description" content="一念 - 浅草寺御神签抽签应用，禅意极简设计，100%吉祥签模式">
<meta name="keywords" content="抽签,御神签,浅草寺,fortune,omikuji">
<meta property="og:title" content="一念 - 浅草寺御神签">
<meta property="og:description" content="禅意极简的抽签应用">
<meta property="og:type" content="website">
```

---

## 🔧 常见问题

### Q1: 图片加载缓慢？

**原因**：图片文件较大（38MB）

**解决方案**：
1. 运行 `optimize_images.py` 压缩图片
2. 使用 Vercel CDN 自动加速
3. 考虑使用图片 CDN 服务（如阿里云 OSS）

### Q2: 路径 404 错误？

**原因**：vercel.json 配置问题

**解决方案**：
确保 `vercel.json` 中的 rewrites 配置正确：
```json
{ "source": "/(.*)", "destination": "/omikuji/$1" }
```

### Q3: 部署后某些资源加载失败？

**原因**：相对路径问题

**解决方案**：
检查 `index.html` 中的资源路径，确保使用相对路径：
```html
<!-- 正确 ✅ -->
<link rel="stylesheet" href="css/styles.css">
<script src="js/app.js"></script>

<!-- 错误 ❌ -->
<link rel="stylesheet" href="/css/styles.css">
```

### Q4: 手机摇一摇不工作？

**原因**：HTTPS 要求

**解决方案**：
- Vercel 自动提供 HTTPS
- 确保使用 HTTPS 访问（Vercel 默认强制 HTTPS）
- iOS 需要在 Safari 中允许运动传感器权限

---

## 📈 部署后优化建议

### 1. 自定义域名

在 Vercel 项目设置中添加自定义域名：
```
yinian.你的域名.com
```

### 2. 环境变量（如需要）

Vercel 项目 → Settings → Environment Variables

### 3. 分析访问数据

使用 Vercel Analytics：
```bash
vercel analytics
```

### 4. 持续部署

推送到 GitHub 后自动部署：
```bash
git add .
git commit -m "更新内容"
git push
```

Vercel 会自动检测并部署最新代码。

---

## 🎯 预期结果

部署成功后，你将获得：

1. **公网访问地址**：`https://yinian-omikuji.vercel.app`
2. **自动 HTTPS**：安全访问
3. **全球 CDN**：快速加载
4. **自动部署**：推送代码即部署
5. **免费托管**：Vercel 免费额度足够使用

---

## 📞 需要帮助？

- Vercel 文档：https://vercel.com/docs
- 项目问题：查看项目 README.md

---

**祝部署顺利！愿每次抽签都带来好运！** 🎲✨
