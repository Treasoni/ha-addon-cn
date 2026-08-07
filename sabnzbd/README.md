<!-- zh-guide -->
# Sabnzbd

## 简介
Sabnzbd 是一款用 C++ 编写的高性能 Usenet（新闻组）下载工具，占用极少的系统资源即可达到很高的下载速度。本加载项致力于让 Usenet 的使用尽可能简单流畅，自动化一切可以自动化的环节。镜像基于 linuxserver/docker-sabnzbd 构建。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/homeassistant
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 sabnzbd 并安装。

## 配置
除以下选项外，其余配置都可以直接在 Sabnzbd 的 WebUI 中完成。

| 配置键 | 类型/默认值 | 说明 |
|--------|------------|------|
| `PUID` | 整数 / `0` | 文件权限使用的用户 ID |
| `PGID` | 整数 / `0` | 文件权限使用的组 ID |
| `TZ` | 字符串（可选） | 时区，例如 `Europe/London` |
| `localdisks` | 字符串（可选） | 要挂载的本地磁盘，例如 `sda1,sdb1,MYNAS` |
| `networkdisks` | 字符串（可选） | 要挂载的 SMB 网络共享，例如 `//SERVER/SHARE` |
| `cifsusername` | 字符串（可选） | SMB 网络共享的用户名 |
| `cifspassword` | 字符串（可选） | SMB 网络共享的密码 |
| `cifsdomain` | 字符串（可选） | SMB 网络共享所属的域 |
| `env_vars` | 数组（可选） | 额外传递给容器的环境变量（名称需匹配 `^[A-Za-z0-9_]+$`） |

本加载项支持挂载本地磁盘与远程 SMB 共享：
- **本地磁盘**：通过 `localdisks` 指定设备名（如 `sda1`）。
- **远程共享**：通过 `networkdisks` 指定 SMB 路径，并配合 `cifsusername`、`cifspassword`、`cifsdomain` 填写凭据。

## 使用 / 访问入口
- **Ingress**：安装并启动后，可直接从 Home Assistant 侧边栏点击 Sabnzbd 图标进入 WebUI（已启用 ingress）。
- **直接访问**：通过浏览器访问 `http://homeassistant:8089`（容器内端口 8080 映射到宿主机 8089）。
- **默认登录**：用户名 `sabnzbd`，密码 `tegbzn6789`。首次进入后请尽快在 WebUI 中修改默认密码。
- **常用操作**：下载任务、新闻组服务器配置、下载目录等设置均在 WebUI 中完成。

## 常见问题
1. **默认登录账号密码是什么？** 用户名 `sabnzbd`，密码 `tegbzn6789`，登录后请及时修改。
2. **如何进入 WebUI？** 可通过 Home Assistant 侧边栏的 Ingress 入口，或访问 `http://homeassistant:8089`。
3. **如何挂载网络磁盘？** 在配置中设置 `networkdisks` 为 SMB 路径，并填写对应的 `cifsusername`、`cifspassword`、`cifsdomain`。

---
- 英文原版：Home assistant add-on: sabnzbd；链接 https://github.com/alexbelgium/hassio-addons/blob/master/sabnzbd/README.md
- 来源仓库：alexbelgium
