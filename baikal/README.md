<!-- zh-guide -->
# Baikal

## 简介

Baikal 是一款轻量级的 CalDAV + CardDAV 服务器，提供丰富的 Web 界面，可方便地管理用户、通讯录（address books）和日历（calendars）。它安装简单、速度快，只需基础 PHP 环境即可运行，数据可存储在 MySQL 或 SQLite 数据库中。本加载项基于 [ckulka/baikal-docker](https://github.com/ckulka/baikal-docker) 镜像构建。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 baikal 并安装。
3. 按偏好设置加载项选项，保存并启动，然后打开 Web 界面完成软件配置。

## 配置

大部分配置通过加载项的 Web 界面完成，加载项侧仅保留以下选项：

| 配置键 | 类型 / 默认值 | 说明 |
| ------ | ----------- | ---- |
| `env_vars` | 列表，默认空 | 附加环境变量，通过此选项传入额外环境变量（变量名大小写均可） |

> 说明：Baikal 的用户、通讯录、日历等均在 Web 界面中管理；加载项配置及自定义数据存放在 `addon_config` 目录下。

## 使用 / 访问入口

- **Web 界面**：启动后打开 http://homeassistant:8013 即可访问（容器端口 `80/tcp`，宿主映射端口 8013），在此完成用户、日历与通讯录的配置。
- **数据存储**：支持 MySQL 或 SQLite 数据库；可配合其他 Home Assistant 加载项使用 CalDAV/CardDAV 协议同步日历与通讯录。

## 常见问题

- **在哪里配置用户和日历？** 全部通过 Web 界面完成，无需修改加载项选项。
- **配置数据存放在哪里？** 存放在 `addon_config` 对应的目录（如 `/addon_configs/` 下），可在支持的文件浏览类加载项中访问，也便于备份。
- **如何接入 iOS/Android 日历与通讯录？** 在设备中按 CalDAV/CardDAV 协议添加账户，填入本加载项的地址与已创建的用户凭据即可同步。

---
- 英文原版：Home assistant add-on: Baikal；链接 https://github.com/alexbelgium/hassio-addons/blob/master/baikal/README.md
- 来源仓库：alexbelgium
