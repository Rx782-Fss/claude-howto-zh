# 快速开始 - 品牌资源

## 将资源复制到你的项目

```bash
# 复制全部资源到 Web 项目
cp -r resources/ /path/to/your/website/

# 或仅复制 Favicon 用于网站
cp resources/favicons/* /path/to/your/website/public/
```

## 添加到 HTML（复制粘贴）

```html
<!-- Favicon -->
<link rel="icon" type="image/svg+xml" href="/resources/favicons/favicon-32.svg" sizes="32x32">
<link rel="icon" type="image/svg+xml" href="/resources/favicons/favicon-16.svg" sizes="16x16">
<link rel="apple-touch-icon" href="/resources/favicons/favicon-128.svg">
<link rel="icon" type="image/svg+xml" href="/resources/favicons/favicon-256.svg" sizes="256x256">
<meta name="theme-color" content="#000000">
```

## 推荐尺寸

| 用途 | 尺寸 | 文件 |
|------|------|------|
| 网站头部 | 520×120 | `logos/claude-howto-logo.svg` |
| 应用图标 | 256×256 | `icons/claude-howto-icon.svg` |
| 浏览器标签 | 32×32 | `favicons/favicon-32.svg` |
| 移动主屏幕 | 128×128 | `favicons/favicon-128.svg` |
| 桌面应用 | 256×256 | `favicons/favicon-256.svg` |
| 小头像 | 64×64 | `favicons/favicon-64.svg` |

## 图标设计含义

**指南针配代码括号**：
- 指南针环 = 导航、结构化学习路径
- 绿色北针 = 方向、进步、指引
- 黑色南针 = 扎根、稳固基础
- `>` 括号 = 终端提示符、代码、CLI 上下文
- 刻度标记 = 精准、结构化步骤

这象征着"通过清晰的指引在代码中找到方向。"
