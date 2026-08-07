<!-- zh-guide -->
# Cloudcommander

## 简介

Cloud Commander 是一个带控制台与编辑器的网页文件管理器。本 add-on 基于 coderaiser 的 cloudcmd 镜像，提供在 Home Assistant 中管理文件的 Web 界面，并可通过 Ingress 在侧边栏访问。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 `cloudcommander` 并安装。
3. 安装完成后启动 add-on，点击「保存」并查看日志确认运行正常。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `env_vars` | 列表 / 空 | 传入容器的额外环境变量（`name`/`value` 形式） |
| `CUSTOM_OPTIONS` | 字符串（可选） / 空 | 自定义 CLI 选项，如 `--name Homeassistant` |
| `DROPBOX_TOKEN` | 字符串（可选） / 空 | Dropbox 集成令牌（见 cloudcmd.io） |
| `smbv1` | 布尔（可选） / 空 | 是否启用 SMB v1 协议 |
| `localdisks` | 字符串（可选） / 空 | 需要挂载的本地磁盘，如 `sda1,sdb1,MYNAS` |
| `networkdisks` | 字符串（可选） / 空 | 需要挂载的 SMB 共享，如 `//SERVER/SHARE` |
| `cifsusername` | 字符串（可选） / 空 | SMB 用户名 |
| `cifspassword` | 字符串（可选） / 空 | SMB 密码 |
| `cifsdomain` | 字符串（可选） / 空 | SMB 域 |

## 使用 / 访问入口

启动后可在 Home Assistant 侧边栏看到 Cloudcommander 图标，点击进入；也可通过 Web 界面端口 8000 直接访问。

## 常见问题

- 除上述选项外，其余配置可在应用的 Web 界面中完成。
- 支持挂载本地磁盘与远程 SMB 共享。
- 可通过 `env_vars` 传入额外环境变量，或通过 addon_config 映射运行自定义脚本。

---
- 英文原版：[Home assistant add-on: Cloudcommander](https://github.com/alexbelgium/hassio-addons/blob/master/cloudcommander/README.md)
- 来源仓库：alexbelgium
