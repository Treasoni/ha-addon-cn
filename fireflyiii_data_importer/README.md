<!-- zh-guide -->
# Firefly iii Data Importer

## 简介
Firefly III 是一款自托管的个人财务管理工具，帮助你记录支出与收入，从而更合理地消费和储蓄。本加载项是专门用于向 Firefly III 导入交易记录的数据导入器，出于安全与维护考虑与 Firefly III 分开部署。本加载项基于 fireflyiii/data-importer 的 Docker 镜像构建。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 fireflyiii_data_importer 并安装。

## 配置
使用前请确保已经有一个正在运行的 Firefly III 实例，并在下面选项中填入实例地址与访问令牌。

| 配置键 | 类型 / 默认值 | 说明 |
|--------|---------------|------|
| `CONFIG_LOCATION` | 字符串 / `/config` | 配置文件位置 |
| `FIREFLY_III_URL` | 字符串（可选） / 空 | Firefly III 实例的地址 |
| `FIREFLY_III_ACCESS_TOKEN` | 字符串 / 空 | Firefly III 的个人访问令牌（必填） |
| `FIREFLY_III_CLIENT_ID` | 字符串（可选） / 空 | OAuth Client ID（访问令牌的替代方案） |
| `NORDIGEN_ID` | 字符串（可选） / 空 | Nordigen Client ID（银行数据集成） |
| `NORDIGEN_KEY` | 字符串（可选） / 空 | Nordigen Client Secret |
| `SPECTRE_APP_ID` | 字符串（可选） / 空 | Spectre/Salt Edge Client ID |
| `SPECTRE_SECRET` | 字符串（可选） / 空 | Spectre/Salt Edge Client Secret |
| `AUTO_IMPORT_SECRET` | 字符串（可选） / 空 | 自动导入 Webhook 的密钥 |
| `CAN_POST_AUTOIMPORT` | 布尔（可选） / 空 | 允许自动导入功能 |
| `CAN_POST_FILES` | 布尔（可选） / 空 | 允许上传文件 |
| `Updates` | 枚举（hourly / daily / weekly）（可选） / 空 | 自动导入计划：每小时 / 每日 / 每周 |
| `silent` | 布尔（可选） / 空 | 抑制调试信息输出 |
| `env_vars` | 列表 / 空 | 额外环境变量（大写或小写命名）；列表项含 `name`（环境变量名，须匹配 `^[A-Za-z0-9_]+$`）与 `value`（环境变量值，可选） |

访问令牌的获取方式：登录 Firefly III → 选项 → 个人资料 → OAuth → 个人访问令牌，创建新令牌并填入 `FIREFLY_III_ACCESS_TOKEN`。

## 使用 / 访问入口
本加载项未启用 Ingress，通过端口访问：容器端口 `8080/tcp` 映射到宿主端口 `3474`，浏览器访问 http://homeassistant:3474 打开 Web 界面。

## 常见问题
1. 需要先有一个可用的 Firefly III 实例，并将地址与访问令牌配置到加载项选项后再启动。
2. 导入配置文件存放于 `/addon_configs/xxx-fireflyiii_data_importer/configurations/`；自动导入时把 CSV 文件放入 `/addon_configs/xxx-fireflyiii_data_importer/import_files/`，并按需设置 `Updates` 计划。
3. 使用自动导入时，需启用 `CAN_POST_AUTOIMPORT` 并设置 `AUTO_IMPORT_SECRET`。
4. 新版本已将配置迁移到 addon_configs 目录（旧路径为 `/config/hassio_addons/fireflyiii_date_importer`），迁移自动完成，请记得更新相关链接。

---
- 英文原版：Home assistant add-on: Fireflyiii data importer；链接 https://github.com/alexbelgium/hassio-addons/blob/master/fireflyiii_data_importer/README.md
- 来源仓库：alexbelgium
