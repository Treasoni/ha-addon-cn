<!-- zh-guide -->
# Calibre

## 简介
Calibre 是一个功能强大且易于使用的电子书管理器，完全免费开源，适合普通用户和资深玩家，可以完成与电子书相关的几乎所有操作。本加载项基于 linuxserver/docker-calibre 镜像构建。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 calibre 并安装。

## 配置
安装后先保存配置，再按需调整下列选项，然后启动加载项：

| 配置键 | 类型/默认值 | 说明 |
|--------|-------------|------|
| `PGID` | int / `0` | 文件权限组 ID |
| `PUID` | int / `0` | 文件权限用户 ID |
| `TZ` | str / 空 | 时区（如 `Europe/London`、`Asia/Shanghai`） |
| `PASSWORD` | str / 空 | 可选的图形界面访问密码 |
| `CLI_ARGS` | str / 空 | 可选的 Calibre 命令行启动参数（如 `--with-library=/books`） |
| `localdisks` | str / 空 | 要挂载的本地磁盘（如 `sda1,sdb1,MYNAS`） |
| `networkdisks` | str / 空 | 要挂载的 SMB 网络共享（如 `//SERVER/SHARE`） |
| `cifsusername` | str / 空 | SMB 共享的用户名 |
| `cifspassword` | str / 空 | SMB 共享的密码 |
| `cifsdomain` | str / 空 | SMB 共享的域 |
| `env_vars` | 数组 / `[]` | 追加的自定义环境变量（name/value 对，键名需为大写或小写字母、数字、下划线） |

配置示例：

```yaml
PGID: 0
PUID: 0
TZ: "Asia/Shanghai"
PASSWORD: "secure-password"
CLI_ARGS: "--with-library=/books"
localdisks: "sda1,sdb1"
networkdisks: "//192.168.1.100/books"
cifsusername: "bookuser"
cifspassword: "password123"
cifsdomain: "workgroup"
```

挂载磁盘：本加载项支持挂载本地磁盘与远程 SMB 共享，分别通过 `localdisks` 与 `networkdisks` 选项启用。自定义脚本和环境变量可通过 `addon_config` 目录及 `env_vars` 选项实现。

## 使用 / 访问入口
- **侧边栏 Ingress**：加载项默认启用 Ingress，可从 Home Assistant 侧边栏直接打开 WebUI（自 8.9.0 起 Ingress 强制走 https）。
- **桌面图形界面**：通过端口 `8181`（https）访问桌面端 GUI。
- **Calibre Web 服务器**：端口 `8081`；**无线连接**：端口 `9090`。这两个功能需在桌面端 GUI 里手动启用。
- WebUI 也可通过 `http://homeassistant:端口` 直接访问。
- 首次使用：启动加载项后打开 WebUI 并按需调整软件选项；数据默认存放在 `/config`（addon_config）。

## 常见问题
- **WebUI 打不开？** Calibre 的 Web 服务器（8081）和无线连接（9090）需要先在桌面图形界面中手动开启；日常使用优先走侧边栏 Ingress 即可。
- **升级后库/路径变了？** 自 7.4.0 起配置数据会自动迁移到 addon_config（`/addon_configs/...-calibre`），并自动处理旧数据，但请同步更新你引用的库路径与链接。
- **想访问 NAS 或本地磁盘？** 在配置中设置 `networkdisks` / `localdisks` 及对应的 cifs 账号信息后重启加载项。

---
- 英文原版：Home assistant add-on: calibre；链接 https://github.com/alexbelgium/hassio-addons/blob/master/calibre/README.md
- 来源仓库：alexbelgium
