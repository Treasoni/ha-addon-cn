<!-- zh-guide -->
# MyElectricalData

## 简介
MyElectricalData 通过 Enedis Gateway API 自动获取你在 Enedis（法国国家电网公司）的电表数据，并将其发送到你的 MQTT Broker，便于在 Home Assistant 中监控用电情况。本项目基于 m4dm4rtig4n/myelectricaldata 构建。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 enedisgateway2mqtt 并安装。

## 配置
首次使用需要先启动一次加载项，以初始化配置模板。主要配置在 `/config/myelectricaldata/config.yaml` 中完成（包括 Enedis API 凭据、MQTT broker 设置、数据获取间隔与设备配置），加载项选项中主要设置以下内容：

| 配置键 | 类型 / 默认值 | 说明 |
|--------|---------------|------|
| `CONFIG_LOCATION` | 字符串 / `/config/myelectricaldata/config.yaml` | 配置文件路径 |
| `TZ` | 字符串（可选） / `Europe/Paris` | 时区，例如 `Europe/London` |
| `mqtt_autodiscover` | 布尔 / `true` | 启用 MQTT 自动发现 |
| `verbose` | 布尔 / `true` | 启用详细日志输出 |
| `env_vars` | 列表 / 空 | 额外环境变量列表（可大写或小写命名），用于覆盖配置 |
| `env_vars.name` | 字符串 | 环境变量名，须匹配 `^[A-Za-z0-9_]+$` |
| `env_vars.value` | 字符串（可选） | 环境变量值 |

## 使用 / 访问入口
启动后可在 Home Assistant 侧边栏看到 MyElectricalData 图标，点击进入。

## 常见问题
1. 需要提前在 Home Assistant 中配置 MQTT 集成（加载项通过 `mqtt:want` 服务检测），否则数据无法发送。
2. 首次启动必须启动一次加载项以生成初始化配置模板，之后在 `/config/myelectricaldata/config.yaml` 中填写 Enedis 凭据与 MQTT 连接信息。
3. 想额外注入环境变量时，可使用 `env_vars` 选项传入，详见 alexbelgium 的 "Add Environment variables to your Addon" wiki。
4. 该加载项已放弃 armv7、armhf 和 i386 架构支持，官方将在 Home Assistant 2025.12 中完全移除。

---
- 英文原版：Home assistant add-on: MyElectricalData；链接 https://github.com/alexbelgium/hassio-addons/blob/master/enedisgateway2mqtt/README.md
- 来源仓库：alexbelgium
