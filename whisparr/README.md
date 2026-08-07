<!-- zh-guide -->
# Whisparr

## 简介

Whisparr 是面向 Usenet 和 BitTorrent 用户的成人视频（Adult）收藏管理工具。它可以监控多个 RSS 源以获取新电影，并与下载客户端和索引器配合完成自动抓取、整理和重命名；当库中出现更高质量的资源时，还能自动把已有文件升级到更好的画质。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 whisparr 并安装。

## 配置

本加载项无需任何配置即可运行。下载客户端、索引器、影片库路径等设置均在 Whisparr 的 Web 界面中完成，首次打开界面时按向导提示填写即可。

## 使用 / 访问入口

启动后，在浏览器中访问 Home Assistant 主机地址的端口 6969 即可打开 Whisparr 界面，并按屏幕向导完成初始设置。

## 常见问题

1. **无法在侧边栏看到本加载项**：本加载项不支持 Home Assistant 的 Ingress（侧边栏）功能，因此只能通过端口 6969 的 Web 界面访问；如需集成到 Home Assistant，可考虑使用 iframe 面板。
2. **首次使用的初始化向导**：第一次打开 Web 界面时需要完成初始化向导（选择下载客户端、索引器与媒体库路径），之后即可自动监控 RSS 并整理影片库。

---
- 英文原版：[Home Assistant Community Add-on: Whisparr](https://github.com/hassio-addons/repository/blob/main/whisparr/README.md)
- 来源仓库：frenck
