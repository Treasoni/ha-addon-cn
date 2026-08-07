<!-- zh-guide -->
# Firefly iii FinTS Importer

## 简介
Firefly III 是一款自托管的个人财务管理工具，帮助你记录支出与收入，从而更合理地消费和储蓄。本加载项用于将支持 FinTS 协议的银行（主要是德国银行）中的交易记录导入 Firefly III，并带有引导式的 Web 界面。本加载项基于 benkl/firefly-iii-fints-importer 的 Docker 镜像构建。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 fireflyiii_fints_importer 并安装。

## 配置
| 配置键 | 类型 / 默认值 | 说明 |
|--------|---------------|------|
| `Updates` | 枚举（hourly / daily2 / daily4 / daily6 / daily8 / daily10 / daily12 / weekly）（可选） / 空 | 自动导入计划：每小时 / 每天2点 / 4点 / 6点 / 8点 / 10点 / 12点 / 每周（周日2点） |
| `silent` | 布尔（可选） / 空 | 抑制调试信息输出 |
| `env_vars` | 列表 / 空 | 额外环境变量（大写或小写命名）；列表项含 `name`（环境变量名，须匹配 `^[A-Za-z0-9_]+$`）与 `value`（环境变量值，可选） |

银行连接与各账户的导入配置在 Web 界面中完成，配置存储于 `/config/addons_config/fireflyiii_fints_importer/`。

## 使用 / 访问入口
本加载项未启用 Ingress，通过端口访问：容器端口 `8080/tcp` 映射到宿主端口 `3476`，浏览器访问 http://homeassistant:3476 打开 Web 界面。

## 常见问题
1. 使用前请确保有一个已运行的 Firefly III 实例。
2. 该导入器支持使用 FinTS（Financial Transaction Services）协议的银行，主要针对德国银行，多数德国主要银行支持通过 FinTS 自动获取交易。
3. 在 Web 界面中为每个银行账户配置连接与导入设置，并按需在 `Updates` 中选择自动导入计划。

---
- 英文原版：Home assistant add-on: Fireflyiii fints importer；链接 https://github.com/alexbelgium/hassio-addons/blob/master/fireflyiii_fints_importer/README.md
- 来源仓库：alexbelgium
