<!-- zh-guide -->
# Elasticsearch server

## 简介

Elasticsearch 是分布式、RESTful 的搜索与分析引擎，是 Elastic Stack 的核心，可用于存储、搜索和管理日志、指标、搜索后端、应用监控、端点安全等数据。本 add-on 以单节点形式运行，供其他需要它的 add-on 调用。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 `elasticsearch` 并安装。
3. 安装完成后启动 add-on，点击「保存」并设置你的偏好选项，然后查看日志确认运行正常。

## 配置

| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `env_vars` | 列表 / 空 | 传入容器的额外环境变量（`name`/`value` 形式）；例如 `ES_SETTING_XPACK_SECURITY_ENABLED=true` 对应 `xpack.security.enabled=true` |

## 使用 / 访问入口

本 add-on 没有 Web 界面，仅提供 API 端点供其他应用调用：HTTP API 端口 9200 用于 REST API 调用，传输端口 9300 用于集群内部通信。单节点集群可通过 `http://<宿主地址>:9200` 访问（默认无认证，仅限本地网络）。

## 常见问题

- 为保持与旧版相同的纯 HTTP 行为（以及与 Home Assistant Elasticsearch 集成的兼容性），`xpack.security.enabled` 默认关闭；如需启用安全功能，可在 `env_vars` 中添加 `ES_SETTING_XPACK_SECURITY_ENABLED=true`。
- 从 7.x 升级到 8.x 是自动且单向的：升级前请先备份，首次启动时 Elasticsearch 会在原地升级现有索引（大数据集可能耗时，切勿在首次启动时停止 add-on）。
- 可通过 `ES_SETTING_<SETTING_WITH_UNDERSCORES>` 形式的环境变量覆盖 Elasticsearch 设置。
- 集成示例：Nextcloud 的全文搜索应用、Home Assistant 的 Elasticsearch 组件。

---
- 英文原版：[Home assistant add-on: elasticsearch server](https://github.com/alexbelgium/hassio-addons/blob/master/elasticsearch/README.md)
- 来源仓库：alexbelgium
