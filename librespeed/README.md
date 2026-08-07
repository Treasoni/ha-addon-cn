<!-- zh-guide -->
# LibreSpeed

## 简介
LibreSpeed 是一个超轻量级的网速测试工具，使用 JavaScript 实现（XMLHttpRequest 与 Web Workers），可自托管带宽测速页面。本加载项基于 linuxserver/docker-librespeed 镜像构建，支持通过侧边栏 Ingress 访问。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 librespeed 并安装。

## 配置
除下表列出的选项外，其余设置可在应用的 WebUI 中完成；默认用户名/密码见启动日志。

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `PGID` | 整数 / 默认 `1000` | 文件权限的用户组 ID |
| `PUID` | 整数 / 默认 `1000` | 文件权限的用户 ID |
| `TZ` | 字符串（可选） | 时区，如 `Europe/London` |
| `PASSWORD` | 字符串（可选） | 可选的结果页访问密码 |
| `CUSTOM_RESULTS` | 布尔 / 默认 `false` | 是否启用自定义结果展示 |
| `IPINFO_APIKEY` | 字符串 / 空 | 可选的 IP 信息 API 密钥 |
| `env_vars` | 列表 / 默认 `[]` | 额外传给容器的环境变量（键名需匹配 `^[A-Za-z0-9_]+$`） |

## 使用 / 访问入口
- 启动后可在 Home Assistant 侧边栏看到 LibreSpeed 图标，点击进入；也可通过浏览器访问宿主端口 8096（对应容器端口 80）。

## 常见问题
- **默认登录信息是什么？** 默认用户名/密码会在启动日志中输出。
- **如何设置访问密码？** 通过 `PASSWORD` 选项设置可选密码；`CUSTOM_RESULTS` 控制是否使用自定义结果页。
- **测速结果与地理位置？** 配置 `IPINFO_APIKEY` 可启用基于 IP 的详情展示。

---
- 英文原版：[Home assistant add-on: librespeed](https://github.com/alexbelgium/hassio-addons/blob/master/librespeed/README.md)
- 来源仓库：alexbelgium
