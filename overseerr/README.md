<!-- zh-guide -->
# Overseerr

## 简介
Overseerr 是一款面向 Plex 生态的观影请求管理与媒体发现工具。用户可以搜索自己想看的影视内容并提交观看请求，方便家庭共享的媒体库统一管理。（当前为实验性初始版本 v0.1.0。）

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/homeassistant
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 overseerr 并安装。

## 配置
本加载项**无需任何配置即可运行**。`config.yaml` 未定义 options/schema，因此没有可配置项；数据读写会自动映射到 `addon_config`、`share`、`media` 等目录。

## 使用 / 访问入口
1. 安装后启动本加载项，并查看日志确认运行正常。
2. 点击加载项页面上的「打开 Web UI」（OPEN WEB UI）按钮进入界面。
3. 也可通过浏览器直接访问 `http://<你的Home Assistant地址>:5055`（端口 5055 已映射）。
4. 首次访问时按屏幕上的向导完成初始化设置，之后即可开始使用。

## 常见问题
- **打开界面后出现设置向导怎么办？** 首次访问会显示初始化向导，按屏幕提示逐步完成即可。
- **如何重新打开界面？** 在加载项页面点击「打开 Web UI」按钮，或访问 `http://<HA地址>:5055`。
- **数据保存在哪里？** 配置文件与媒体数据通过 `addon_config`、`share`、`media` 映射目录持久化，请勿随意改动容器内路径。

---
- 英文原版：Home Assistant Community Add-on: Overseerr
  链接：https://github.com/hassio-addons/repository/blob/master/overseerr/README.md
- 来源仓库：frenck
