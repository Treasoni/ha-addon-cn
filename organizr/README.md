<!-- zh-guide -->
# Organizr

## 简介

Organizr 是一款用 PHP 编写的 HTPC/家庭实验室服务组织器，它把 Plex、Radarr、Sonarr 等各类服务统一收纳到一个漂亮的 Web 门户中，方便你集中管理所有自托管服务的标签页与访问入口。本加载项基于 linuxserver.io 的 Organizr Docker 镜像构建。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 organizr 并安装。

## 配置

Organizr 在加载项选项中只需要很少的配置，大多数设置（服务集成、认证、主题等）都在 Web 界面中完成。可配置选项如下：

| 配置键 | 类型 / 默认值 | 说明 |
| ------ | ------------- | ---- |
| `PUID` | 整数，默认 `1000` | 文件权限的用户 ID |
| `PGID` | 整数，默认 `1000` | 文件权限的用户组 ID |
| `branch` | 枚举 `list(v2-master\|v2-develop)`，默认 `v2-master` | 使用的 Organizr 分支，`v2-master` 为稳定版，`v2-develop` 为开发版 |
| `env_vars` | 列表（可选） | 附加环境变量列表，每项包含 `name`（变量名）与 `value`（变量值），用于向容器传入额外环境变量 |

## 使用 / 访问入口

启动后打开 Web 界面（端口 `80/tcp` 映射到宿主端口 `88`，访问 `http://homeassistant.local:88`）。首次使用按以下步骤设置：

1. 打开 Web 界面，按照设置向导创建管理员账号。
2. 在 Web 界面中添加和配置你的服务与标签页。
3. 数据库文件保存在 `/data/` 目录中。

## 常见问题

- **如何开始使用？** 启动加载项并访问 Web 界面，按向导创建管理员账号，然后添加你的各类服务入口即可。
- **需要配置很多选项吗？** 不需要。Organizr 大多数功能（服务集成、认证、主题）都在 Web 界面中配置，加载项选项只需设置文件权限与分支即可。
- **数据库存在哪里？** 数据库文件保存在 `/data/` 目录中，升级后会保留。
- **想用开发版功能？** 将 `branch` 选项改为 `v2-develop` 即可使用开发分支，但可能有稳定性风险。
- **如何传递自定义环境变量？** 使用 `env_vars` 选项，每项填写 `name` 与 `value`。

---
- 英文原版：Home assistant add-on: Organizr；链接 https://github.com/alexbelgium/hassio-addons/blob/master/organizr/README.md
- 来源仓库：alexbelgium
