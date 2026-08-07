<!-- zh-guide -->
# BentoPDF

## 简介

BentoPDF 是一款注重隐私的 PDF 工具箱，提供 50 多种处理工具，全部在浏览器内通过 WebAssembly 在本地完成处理——无需上传、无需云端、无任何追踪。所有文件都不会离开你的设备。本加载项把 BentoPDF 的 Web 应用托管在 Home Assistant 上，让你在局域网内任意位置都能访问。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 bentopdf 并安装。
3. 保存配置并启动加载项，然后打开 Web 界面即可使用。

## 配置

除日志级别外无需其他配置，放入文件即可使用：

| 配置键 | 类型 / 默认值 | 说明 |
| ------ | ----------- | ---- |
| `log_level` | 枚举 `info\|debug\|warn\|error`，默认 `info` | 日志详细程度：`info` 常规日志；`debug` 调试日志；`warn` 警告；`error` 仅记录错误 |

## 使用 / 访问入口

- **Web 界面**：启动后打开 https://homeassistant:8443 即可访问（容器端口 `8443/tcp` 映射到宿主端口 8443，HTTPS Web 界面）。
- **HTTP 入口**：容器端口 `8080/tcp` 映射到宿主端口 8080，用于 watchdog 健康检查并自动跳转到 HTTPS。

## 常见问题

- **文件会上传到服务器吗？** 不会。所有 PDF 处理（合并、拆分、转换、OCR、加密等）都在浏览器本地通过 WebAssembly 完成，文件从不离开你的设备。
- **可以离线使用吗？** 页面加载完成后可完全离线工作，无遥测、无分析、无外部请求。
- **支持哪些格式转换？** 支持 Word、Excel、PowerPoint、图片、Markdown、HTML、CSV、EPUB、MOBI 等数十种格式转 PDF，也支持 PDF 转 DOCX、JPG、PNG、Text、JSON 等，以及加密、签名、水印、压缩、OCR 等高级功能。

---
- 英文原版：Home assistant add-on: BentoPDF；链接 https://github.com/alexbelgium/hassio-addons/blob/master/bentopdf/README.md
- 来源仓库：alexbelgium
