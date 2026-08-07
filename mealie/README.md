<!-- zh-guide -->
# Mealie

## 简介
Mealie 是一款自托管的菜谱管理与膳食计划工具，基于 Vue 构建，提供 RestAPI 后端与响应式前端，界面友好，适合全家共同管理菜谱、规划每日膳食。本加载项基于 hendrix04 的 mealie-combined 镜像（对应 Mealie 1.0 及以上版本）。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 mealie 并安装。

## 配置
除下表列出的选项外，大部分配置可直接在 Mealie 的 Web 界面中完成。

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `PGID` | int / `1000` | 文件权限组 ID |
| `PUID` | int / `1000` | 文件权限用户 ID |
| `ssl` | bool / `false` | 为 Web 界面启用 HTTPS |
| `certfile` | str / `fullchain.pem` | SSL 证书文件（须位于 /ssl）|
| `keyfile` | str / `privkey.pem` | SSL 私钥文件（须位于 /ssl）|
| `BASE_URL` | str / 空 | 可选的外部访问基础 URL |
| `DATA_DIR` | str / `/config` | 数据目录路径 |
| `ALLOW_SIGNUP` | bool / `true` | 是否允许新用户注册 |
| `env_vars` | array / 空 | 以键值对列表向应用传递额外环境变量（键名匹配 `[A-Za-z0-9_]+`）|
| `FORWARDED_ALLOW_IPS` | str / 空 | Gunicorn 的 `--forwarded-allow-ips` 设置，用于受信任的反向代理（逗号分隔的 IP，例如 `192.168.1.1,10.0.0.1`）；为隐藏选项，默认不在选项页显示 |

补充说明：
- 可通过在 `/homeassistant/addons_config/xxx-mealie/config.yaml` 中添加环境变量来扩展配置。
- 完整后端配置项见 Mealie 官方文档：https://nightly.mealie.io/documentation/getting-started/installation/backend-config/

## 使用 / 访问入口
- Web 界面可通过 http://homeassistant:9090 访问（容器端口 9001 映射到宿主机 9090），也可通过 Home Assistant 侧边栏的 Ingress 入口打开。
- 首次登录默认凭据：
  - 用户名：`changeme@example.com`
  - 密码：`MyPassword`
- 启动后请先查看日志确认无错误；安装完成后即可开始添加菜谱、规划每周膳食。
- 可与 Home Assistant 集成：通过 REST 传感器读取“今日菜单”等数据（详见上游文档）。

## 常见问题
- 忘记默认登录信息？默认用户名为 `changeme@example.com`、密码为 `MyPassword`，登录后建议立即修改。
- armv7 架构仅支持到 0.4.3 版本，后续版本不再更新。
- 启用 `ssl: true` 前，请先确保 certfile / keyfile 指向 /ssl 目录下正确的证书文件，否则 Web 界面可能无法通过 HTTPS 访问。

---
- 英文原版：Hass.io Add-ons: Mealie；链接 https://github.com/alexbelgium/hassio-addons/blob/master/mealie/README.md
- 来源仓库：alexbelgium
