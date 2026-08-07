<!-- zh-guide -->
# Vaultwarden（Bitwarden RS）

## 简介
Vaultwarden 是一款开源密码管理方案（基于轻量级的 Bitwarden RS 实现），可将网站账号密码等敏感信息加密存储在自己的保险库中。本加载项是官方 Bitwarden 加载项的社区分支，支持通过 Web 界面、桌面端、浏览器扩展和移动 App 等多种客户端访问。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 bitwarden 并安装。
3. 启动加载项，并查看日志确认运行正常（日志中会显示管理员令牌）。

## 配置
| 配置键 | 类型/默认值 | 说明 |
| --- | --- | --- |
| ssl | 布尔值，默认 `true` | 是否启用 SSL（HTTPS）。仅对直接访问生效，对 Ingress 无效。 |
| certfile | 字符串，默认 `fullchain.pem` | SSL 证书文件，必须放在 `/ssl/` 目录下。 |
| keyfile | 字符串，默认 `privkey.pem` | SSL 私钥文件，必须放在 `/ssl/` 目录下。 |
| log_level | 可选：`trace`/`debug`/`info`/`notice`/`warning`/`error`/`fatal` | 日志级别，默认 `info`，调试问题时可调高。 |
| request_size_limit | 整数，可选 | API 请求大小上限（字节），默认 10MB（10485760）。需要大批量导入时可调大，也可调小以防滥用。 |
| env_vars | 键值对数组，可选 | 传入额外的环境变量，格式为 `{"name": "变量名", "value": "值"}`。 |

修改配置后需重启加载项生效。

## 使用 / 访问入口
- 该加载项**不支持 Ingress**（受 Bitwarden Vault Web 界面技术限制）。
- 直接访问：浏览器打开 `http://<主机地址>:7277`（启用 SSL 时用 `https://<主机地址>:7277`），首次访问需注册账号。
- 管理后台：在地址后追加 `/admin`，例如 `https://hassio.local:7277/admin`，使用日志中的管理员令牌登录。
- 管理员令牌只在首次启动且尚未保存配置时显示在日志中；在管理后台保存或修改任意设置后即不再显示，请及时妥善保存。

## 常见问题
- **管理员令牌丢失？** 首次启动时日志会打印临时随机令牌，请尽快登录 `/admin` 后台修改并保存；令牌只显示一次。
- **浏览器报 `Cannot read property 'importKey'`？** 某些浏览器（如 Chrome）禁止在不安全上下文（HTTP）下使用 Web Crypto API，请启用 SSL 并通过 HTTPS 访问。
- **无法大批量导入？** 默认 API 请求上限为 10MB，可通过 `request_size_limit` 配置调整。

---
- 英文原版：Home assistant add-on: Vaultwarden (Bitwarden RS)；链接 https://github.com/alexbelgium/hassio-addons/blob/master/bitwarden/README.md
- 来源仓库：alexbelgium
