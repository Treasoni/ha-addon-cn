<!-- zh-guide -->
# Gitea

## 简介
Gitea 是一款轻量、易用的自托管一体化软件开发服务，集 Git 代码托管、代码审查、团队协作、软件包仓库与 CI/CD 于一体，功能类似 GitHub、Bitbucket 和 GitLab。本加载项基于官方 gitea/gitea 容器镜像打包，并针对 Home Assistant 做了配置适配（SSL、域名、Root URL、app.ini 直接编辑等）。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 gitea 并安装。

## 配置
大部分设置可直接在 Gitea 的 Web 界面完成，以下选项需通过加载项配置页设置：

| 配置键 | 类型/默认值 | 说明 |
|--------|------|------|
| `ssl` | bool / `false` | 是否为 Web 界面启用 HTTPS |
| `certfile` | str / `fullchain.pem` | SSL 证书文件（必须位于 /ssl 目录） |
| `keyfile` | str / `privkey.pem` | SSL 私钥文件（必须位于 /ssl 目录） |
| `APP_NAME` | str / `Gitea for Homeassistant` | Gitea 应用名称 |
| `DOMAIN` | str / `homeassistant.local` | 访问域名 |
| `ROOT_URL` | str / 可选 | 自定义根 URL（用于特殊路由需求）；不设置时加载项会根据协议、DOMAIN 与端口自动推导 |
| `env_vars` | 数组 / `[]` | 向容器传入额外环境变量（变量名大小写均可） |

示例配置：

```yaml
ssl: false
certfile: "fullchain.pem"
keyfile: "privkey.pem"
APP_NAME: "Gitea for Homeassistant"
DOMAIN: "homeassistant.local"
ROOT_URL: "http://homeassistant.local:3000"
```

### 直接编辑 app.ini
Gitea 的 `app.ini` 配置文件已暴露到加载项配置目录（宿主机上的 `/addon_configs/gitea/app.ini`），可直接用 HA 文件编辑器或 Studio Code 加载项修改。

- **首次运行**：先完成 Gitea 的初始化向导，然后重启加载项，生成的 `app.ini` 会自动复制到该目录。
- **后续运行**：任何选项未覆盖到的 Gitea 设置，直接编辑 `app.ini` 即可；`ssl`、`certfile`、`keyfile`、`APP_NAME`、`DOMAIN`、`ROOT_URL` 这些加载项选项会在每次重启时覆盖写入。

完整参数见 [Gitea 配置速查表](https://docs.gitea.com/administration/config-cheat-sheet)。

## 使用 / 访问入口
- **Ingress**：可通过 Home Assistant 侧边栏直接访问。
- **Web 界面**：`http://homeassistant:3000`（对应配置中的 webui 为 `[PROTO:ssl]://[HOST]:[PORT:3000]`）。
- **端口**：`3000/tcp` 为 Web 界面，`22/tcp` 映射到宿主机的 `2222` 端口用于 SSH。
- **首次访问**：打开 Web 界面完成初始化向导（创建管理员账号），随后重启加载项使各项选项生效。

## 常见问题
**想修改 Gitea 的完整配置怎么办？**
编辑宿主机 `/addon_configs/gitea/app.ini`，重启加载项后生效；加载项选项（SSL、DOMAIN、ROOT_URL、APP_NAME）会在每次重启时覆盖写入该文件。

**启用 ssl 后需要准备什么？**
证书文件（`certfile`/`keyfile`）需放在 `/ssl` 目录；开启 `ssl` 后 Web 界面即走 HTTPS。1.27 起健康检查在 HTTPS 环境下也能正常工作，Home Assistant 可准确上报加载项状态。

**SSH 推送报错 `chroot("/var/empty"): Operation not permitted`？**
这是旧版本 AppArmor 权限问题，升级到 1.26.2-1 及以上版本即可解决。

---
- 英文原版：Home assistant add-on: Gitea
- 链接：https://github.com/alexbelgium/hassio-addons/blob/master/gitea/README.md
- 来源仓库：alexbelgium
