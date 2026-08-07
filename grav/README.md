<!-- zh-guide -->
# Grav web server

## 简介
Grav 是一款免费、自托管的开源内容管理系统（CMS），使用 PHP 编写并基于 Symfony Web 应用框架，前后端均采用扁平文件数据库，兼具快速、简单与灵活的特点。本加载项基于 linuxserver/docker-grav 镜像构建。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 grav 并安装。

## 配置
大部分配置可通过 Grav 的 Web 界面完成，只有以下选项需要在加载项选项中设置：

| 配置键 | 类型 / 默认值 | 说明 |
|--------|---------------|------|
| `PGID` | 整数 / `1000` | 文件权限的组 ID |
| `PUID` | 整数 / `1000` | 文件权限的用户 ID |
| `TZ` | 字符串（可选） / 空 | 时区，例如 `Europe/London` |
| `env_vars` | 列表 / 空 | 额外环境变量（大写或小写命名） |
| `env_vars.name` | 字符串 | 环境变量名，须匹配 `^[A-Za-z0-9_]+$` |
| `env_vars.value` | 字符串（可选） | 环境变量值 |

## 使用 / 访问入口
本加载项未启用 Ingress，通过端口访问：容器端口 `80/tcp` 映射为宿主端口 9191，浏览器访问 http://homeassistant:9191 打开 Web 界面。首次启动后按 Grav 的设置向导完成初始化。

## 常见问题
1. 自定义主题与骨架可放入 `/share/grav/www/user/` 目录：主题在 `themes/`，插件在 `plugins/`，页面在 `pages/`。
2. 主题与插件可通过管理面板安装；站点的具体配置在 Web 界面中完成。

---
- 英文原版：Home assistant add-on: Grav；链接 https://github.com/alexbelgium/hassio-addons/blob/master/grav/README.md
- 来源仓库：alexbelgium
