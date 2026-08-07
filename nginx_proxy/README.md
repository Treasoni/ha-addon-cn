<!-- zh-guide -->
# NGINX Home Assistant SSL 代理

## 简介
基于 NGINX 的 SSL/TLS 反向代理加载项。它对外提供 SSL 加密访问，同时允许 Home Assistant 内部保持非加密通信，是搭建 HTTPS 远程访问的常用组件。一般与 Duck DNS、Let's Encrypt 配合使用，为你的域名生成并加载证书。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 nginx_proxy 并安装。

## 配置
| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| domain | str，必填 | 代理使用的完整域名，需解析到本机公网地址 |
| hsts | str，默认 `max-age=31536000; includeSubDomains` | 发送的 `Strict-Transport-Security` 响应头值；留空则不发送 |
| certfile | str，默认 `fullchain.pem` | 位于 `/ssl` 目录的证书文件 |
| keyfile | str，默认 `privkey.pem` | 位于 `/ssl` 目录的私钥文件 |
| cloudflare | bool，默认 `false` | 启用后自动从 Cloudflare 获取 IP 列表写入 `set_real_ip_from` 指令，用于正确识别真实访客 IP |
| use_ssl_backend | bool，默认 `false` | 当 Home Assistant 的 `http` 段使用了 `ssl_certificate`/`ssl_key` 时，启用后 Nginx 以 SSL 方式连接后端 |
| client_max_body_size_megabytes | int，默认 `1` | 允许的最大客户端请求体体积（单位 MB）；设为 `0` 表示不限制（可用于上传大文件） |
| customize.active | bool，默认 `false` | 启用后从 `/share` 目录读取额外的自定义 Nginx 配置片段 |
| customize.default | str，默认 `nginx_proxy_default*.conf` | 默认服务器的 Nginx 配置文件，位于 `/share` 目录 |
| customize.servers | str，默认 `nginx_proxy/*.conf` | 附加服务器的 Nginx 配置文件，位于 `/share` 目录 |
| real_ip_from | list[str]，默认 `[]` | 启用 TCP PROXY 协议并指定信任的上游 IP，用于从负载均衡器获取真实 IP |

端口：`443/tcp`（HTTPS，默认 443）；`443/udp`（HTTP/3 QUIC，默认关闭，设为与 HTTPS 相同的端口即可启用 HTTP/3）；`80/tcp`（HTTP，默认关闭）。

## 使用 / 访问入口
1. 先用 Duck DNS 或 Let's Encrypt 为域名生成证书，并确认证书文件已存放到 `/ssl` 目录（默认名为 `fullchain.pem` 与 `privkey.pem`）。
2. 在 Home Assistant 的 `configuration.yaml` 中为 `http` 段添加反向代理信任配置，否则经代理访问会返回 400：

   ```yaml
   http:
     use_x_forwarded_for: true
     trusted_proxies:
       - 172.30.33.0/24
   ```

3. 在加载项配置中把 `domain` 改为你的注册域名，其余选项保持默认。
4. 保存配置并启动加载项，等待片刻后查看日志确认运行正常。
5. 之后通过 `https://你的域名` 访问 Home Assistant；访问 80 端口会自动 301 跳转到 HTTPS。

## 常见问题
- **访问返回 `400 Bad Request`**：通常是因为缺少 `trusted_proxies` 配置，按上文在 Home Assistant 的 `http` 段补上即可。
- **HTTP/3 (QUIC) 不生效**：在浏览器开发者工具中检查响应头是否有 `Alt-Svc 'h3=":443"; ma=86400'`，并确认防火墙放行了 UDP QUIC 端口。另外 HTTP/3 下无法转发客户端地址中的端口，若 Home Assistant 运行在非 443 端口，会影响校验请求 Host/端口的功能（如 MCP 客户端的 OAuth2 发现端点），建议使用默认 443 端口或关闭 HTTP/3。
- **端口 80 默认被禁用**：这是为了把 80 端口留给 `emulated_hue` 等其它组件使用。

---
- 英文原版：Home Assistant App: NGINX Home Assistant SSL proxy；链接 https://github.com/home-assistant/addons/blob/master/nginx_proxy/README.md
- 来源仓库：official
