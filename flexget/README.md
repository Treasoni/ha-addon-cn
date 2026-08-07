<!-- zh-guide -->
# Flexget

## 简介
FlexGet 是一款多用途媒体自动化工具，可处理 torrent、NZB、播客、漫画、电视、电影、RSS、HTML、CSV 等多种来源。它拥有强大的插件系统（300+ 插件），支持 RSS 抓取与过滤、与下载客户端集成、基于 Web 的管理界面以及定时执行与守护进程模式。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 flexget 并安装。

## 配置
FlexGet 的 YAML 配置文件位于 `/config/flexget/config.yml`，用于定义任务、RSS 源与下载客户端等。加载项提供以下选项：

| 配置键 | 类型 / 默认值 | 说明 |
|--------|---------------|------|
| `PGID` | 整数 / `0` | 文件权限的组 ID |
| `PUID` | 整数 / `0` | 文件权限的用户 ID |
| `WebuiPass` | 字符串（可选） / `homeassistant123` | Web 界面密码 |
| `FG_PLUGINS` | 字符串（可选） / 空 | 额外安装的插件包 |
| `FG_LOG_LEVEL` | 枚举（critical / error / warning / info / verbose / debug / trace）（可选） / 空 | 日志级别 |
| `env_vars` | 列表 / 空 | 额外环境变量（大写或小写命名） |
| `env_vars.name` | 字符串 | 环境变量名，须匹配 `^[A-Za-z0-9_]+$` |
| `env_vars.value` | 字符串（可选） | 环境变量值 |

## 使用 / 访问入口
本加载项未启用 Ingress，通过端口访问：容器端口 `5050/tcp` 映射到宿主端口 `5050`，浏览器访问 http://homeassistant:5050 打开 Web 界面。

## 常见问题
1. Web 界面默认密码为 `homeassistant123`，建议在加载项选项（`WebuiPass`）中修改。
2. 主要配置在 `/config/flexget/config.yml` 中完成，可在其中定义任务、RSS 源与输出插件。
3. `FG_PLUGINS` 可安装额外的插件包（如 `flexget-plugins-extra`），用于扩展功能。

---
- 英文原版：Hass.io Add-ons: Flexget；链接 https://github.com/alexbelgium/hassio-addons/blob/master/flexget/README.md
- 来源仓库：alexbelgium
