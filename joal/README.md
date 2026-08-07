<!-- zh-guide -->
# Joal

## 简介
Joal 是一个开源的命令行 RatioMaster，带 WebUI，可模拟 BT 客户端的上传流量，用于提升种子 Ratio。本加载项基于 anthonyraymond/joal 的 Docker 镜像构建，支持通过侧边栏 Ingress 访问。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 joal 并安装。

## 配置
除下表列出的选项外，其余设置可在加载项日志与 WebUI 中完成。

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `secret_token` | 字符串 / 默认 `lrMY24Byhx` | Web 界面访问的认证令牌，建议修改为自定义值 |
| `ui_path` | 字符串 / 默认 `joal` | Web UI 路径 |
| `run_duration` | 字符串 / 默认 `12h` | 运行时长，如 `5s`、`2m`、`12h`、`5d`，到期自动停止 |
| `verbose` | 布尔（可选） | 是否输出详细日志 |
| `env_vars` | 列表 / 默认 `[]` | 额外传给容器的环境变量（键名需匹配 `^[A-Za-z0-9_]+$`） |

## 使用 / 访问入口
- 启动后可在 Home Assistant 侧边栏看到 Joal 图标，点击进入；也可通过浏览器访问宿主端口 8091（对应容器端口 8081）。
- BT 流量端口 49152 可选，如使用请在路由器上开放相关端口。

## 常见问题
- **Web 界面如何登录？** 打开 WebUI 时使用 `secret_token` 作为认证令牌，登录信息与配置详情会在加载项日志中提示。
- **需要开放哪些端口？** 建议在路由器上开放 Web UI 宿主端口 8091 与 BT 流量端口 49152。
- **如何自动停止？** 通过 `run_duration` 设置运行时长（如 `12h`），到期后 Joal 会自动停止。

---
- 英文原版：[Home assistant add-on: Joal](https://github.com/alexbelgium/hassio-addons/blob/master/joal/README.md)
- 来源仓库：alexbelgium
