<!-- zh-guide -->
# Xteve

## 简介

xTeVe 是用于 Plex DVR 与 Emby Live TV 的 M3U 代理，它将来自各类 IPTV 源的 M3U 播放列表与 XMLTV 节目单统一转换为 Plex/Emby 可用的形式，方便你在媒体服务器中收看 IPTV 直播频道。本加载项基于 collelog/xteve 镜像构建，项目主页：https://github.com/xteve-project/xTeVe

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 xteve 并安装。

## 配置

本加载项的选项很少，绝大多数设置通过 Web 界面完成。修改配置后需要重启加载项才能生效。

| 配置键 | 类型/默认值 | 说明 |
| ------ | ----------- | ---- |
| `env_vars` | 列表，默认空 | 传入容器的自定义环境变量列表，每项包含 `name`（变量名，须匹配 `^[A-Za-z0-9_]+$`）与 `value`（变量值，可选）。 |

## 使用 / 访问入口

本加载项不提供 Ingress，通过端口访问：

- Web 界面容器端口 `34400/tcp`，宿主端口 34400，访问路径为 `/web`（例如 `你的HomeAssistant地址:34400/web`）。
- 配置数据存放在 `/data/` 目录。在 Web 界面中配置 M3U 播放列表与 XMLTV 节目单来源，随后即可在 Plex/Emby 中使用。

## 常见问题

- **为什么加载项选项那么少？** xTeVe 的配置几乎全部在 Web 界面（端口 34400）中完成，加载项层面无需额外配置。
- **配置存放在哪里？** xTeVe 的配置保存在 `/data/` 目录（环境变量 `XTEVE_CONF`/`XTEVE_HOME` 指向该目录），升级前建议做好备份。
- **需要自定义环境变量？** 通过 `env_vars` 选项传入（变量名支持大小写），参见上游 wiki「Add environment variables to your add-on」。
- 自 2.5.3-3 版本起新增 `env_vars` 选项；从 2.2.0.200 起支持配置持久化。
- Home Assistant 项目已弃用 armv7、armhf 与 i386 架构支持，将在 Home Assistant 2025.12 版本中完全移除。

---
- 英文原版：Home assistant add-on: xTeVe；链接 https://github.com/alexbelgium/hassio-addons/blob/master/xteve/README.md
- 来源仓库：alexbelgium
