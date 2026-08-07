<!-- zh-guide -->
# Aurral

## 简介

Aurral 是一款自托管的音乐发现与点播管理应用，为 Lidarr 提供服务，支持点单（request）管理、流程（flows）与播放列表导入，并能基于音乐库进行智能推荐。它基于 [lklynet/aurral](https://github.com/lklynet/aurral) 镜像构建。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 aurral 并安装。
3. 保存配置，将 `download_folder` 设为你偏好的路径，可选设置 `weekly_flow_folder`。
4. 启动加载项，打开 Web 界面完成首次引导（onboarding）。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
| ------ | ----------- | ---- |
| `download_folder` | 字符串，默认 `/share/aurral/downloads` | Aurral 写入流程下载（flow downloads）文件的路径，必须位于 `/share` 目录下 |
| `weekly_flow_folder` | 字符串，默认 `weekly-flow` | 每周流程文件的子文件夹名，追加在 `download_folder` 之后；完整路径为 `download_folder/weekly_flow_folder` |

## 使用 / 访问入口

- **Web 界面**：启动后打开 http://homeassistant:3001（容器端口 `3001/tcp` 映射到宿主端口 `3001`），首次访问需完成 onboarding 引导。
- 加载项映射了 `addon_config`、`share` 与 `media` 目录用于持久化与数据访问。

## 常见问题

- **`download_folder` 必须填 `/share` 下吗？** 是的，上游要求流程下载路径必须位于 `/share` 目录下，否则无法写入。
- **每周流程文件存放在哪里？** 存放在 `download_folder/weekly_flow_folder`，例如默认的 `/share/aurral/downloads/weekly-flow`。
- **首次打开 Web 界面该做什么？** 按 onboarding 引导完成初始配置，接入你的 Lidarr 实例后再使用推荐与点单功能。

---
- 英文原版：Aurral；链接 https://github.com/alexbelgium/hassio-addons/blob/master/aurral/README.md
- 来源仓库：alexbelgium
