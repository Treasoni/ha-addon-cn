<!-- zh-guide -->
# Mylar3

## 简介
mylar3 是一个自动化漫画书（cbr/cbz）下载工具，配合 NZB 与 BT 下载器使用，支持 SABnzbd、NZBGET、多种 BT 客户端以及 DDL。本加载项基于 linuxserver/docker-mylar3 镜像构建。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 mylar3 并安装。

## 配置
除下表列出的选项外，其余设置可在应用的 WebUI 中完成。

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `PGID` | 整数 / 默认 `0` | 文件权限的用户组 ID |
| `PUID` | 整数 / 默认 `0` | 文件权限的用户 ID |
| `TZ` | 字符串（可选） | 时区，如 `Europe/London` |
| `localdisks` | 字符串（可选） | 要挂载的本地磁盘，如 `sda1,sdb1,MYNAS` |
| `networkdisks` | 字符串（可选） | 要挂载的 SMB 共享，如 `//SERVER/SHARE` |
| `cifsusername` | 字符串（可选） | SMB 网络共享用户名 |
| `cifspassword` | 字符串（可选） | SMB 网络共享密码 |
| `cifsdomain` | 字符串（可选） | SMB 网络共享域/工作组 |
| `env_vars` | 列表 / 默认 `[]` | 额外传给容器的环境变量（键名需匹配 `^[A-Za-z0-9_]+$`） |

## 使用 / 访问入口
- 通过浏览器访问宿主端口 8090 打开 Web 界面，在界面中配置下载器与漫画来源。

## 常见问题
- **如何挂载媒体目录？** 可通过 `localdisks` 挂载本地磁盘，或通过 `networkdisks` 挂载远程 SMB 共享（配合 `cifsusername`/`cifspassword`/`cifsdomain`）。
- **更多配置？** 其余选项可直接在应用的 WebUI 中调整。

---
- 英文原版：[Home assistant add-on: mylar3](https://github.com/alexbelgium/hassio-addons/blob/master/mylar3/README.md)
- 来源仓库：alexbelgium
