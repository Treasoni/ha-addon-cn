<!-- zh-guide -->
# Gazpar2mqtt

## 简介
Gazpar2mqtt 是一个 Python 脚本，用于从 GRDF（法国燃气公司）获取燃气消耗数据，并发布到 MQTT Broker，便于在 Home Assistant 中监控燃气使用情况。本项目基于 ssenart/gazpar2mqtt 构建。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 gazpar2mqtt 并安装。

## 配置
主要配置在 `/config/gazpar2mqtt/config.yaml` 中完成（包括 GRDF 账户凭据、MQTT broker 设置、数据获取间隔等）。加载项选项如下：

| 配置键 | 类型 / 默认值 | 说明 |
|--------|---------------|------|
| `CONFIG_LOCATION` | 字符串 / `/config/gazpar2mqtt/config.yaml` | 配置文件路径 |
| `TZ` | 字符串（可选） / `Europe/Paris` | 时区，例如 `Europe/London` |
| `mqtt_autodiscover` | 布尔 / `true` | 启用 MQTT 自动发现 |
| `verbose` | 布尔 / `true` | 启用详细日志输出 |
| `env_vars` | 列表 / 空 | 额外环境变量（大写或小写命名）；列表项含 `name`（环境变量名，须匹配 `^[A-Za-z0-9_]+$`）与 `value`（环境变量值，可选） |

在配置文件 `config.yaml` 中填写 GRDF 凭据（`grdf` 的 username/password）与 MQTT 连接信息（`mqtt` 的 host/port/username/password/topic_prefix），并可设置 `update_frequency`（单位秒）控制更新频率。

## 使用 / 访问入口
本加载项没有 Web 界面，也不映射端口。它以后台脚本方式从 GRDF 获取燃气数据并通过 MQTT 发布，数据可通过 Home Assistant 的 MQTT 集成（自动发现）直接查看。

## 常见问题
1. 需要先在 https://monespace.grdf.fr/ 注册一个 GRDF 账户，并把凭据填入配置文件的 `grdf` 部分。
2. 需要提前在 Home Assistant 中配置 MQTT 集成（加载项通过 `mqtt:want` 服务检测），否则数据无法发布。
3. 该加载项已放弃 armv7、armhf 和 i386 架构支持，官方将在 Home Assistant 2025.12 中完全移除。

---
- 英文原版：Home assistant add-on: gazpar2mqtt；链接 https://github.com/alexbelgium/hassio-addons/blob/master/gazpar2mqtt/README.md
- 来源仓库：alexbelgium
