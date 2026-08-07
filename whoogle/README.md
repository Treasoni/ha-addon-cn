<!-- zh-guide -->
# Whoogle Search

## 简介

Whoogle Search 是一款自托管、无广告、注重隐私的元搜索引擎，让你可以在不受跟踪与广告干扰的情况下使用搜索引擎。本加载项基于 benbusby/whoogle-search 镜像构建。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 whoogle 并安装。

## 配置

除下列选项外，其余设置可通过应用自身的 Web 界面完成。修改配置后需要重启加载项才能生效。

| 配置键 | 类型/默认值 | 说明 |
| ------ | ----------- | ---- |
| `env_vars` | 列表，默认空 | 传入容器的自定义环境变量列表，每项包含 `name`（变量名，须匹配 `^[A-Za-z0-9_]+$`）与 `value`（变量值，可选）。 |
| `TZ` | 字符串，默认 `Europe/Amsterdam` | 时区。 |
| `WHOOGLE_CONFIG_LANGUAGE` | 字符串，默认 `lang_en` | 界面语言（如 `lang_en`、`lang_zh` 等）。 |
| `WHOOGLE_CONFIG_URL` | 字符串，默认 `https://website.com` | 服务的对外访问地址（Base URL）。 |
| `WHOOGLE_CONFIG_THEME` | 枚举（system/light/dark），默认空 | 界面主题：跟随系统/浅色/深色。 |
| `WHOOGLE_CONFIG_COUNTRY` | 可选字符串，默认空 | 搜索结果的国家代码。 |
| `WHOOGLE_CONFIG_SEARCH_LANGUAGE` | 可选字符串，默认空 | 搜索语言。 |
| `WHOOGLE_CONFIG_NEAR` | 可选字符串，默认空 | 搜索结果的定位地区/邻近参数，可留空。 |
| `WHOOGLE_CONFIG_BLOCK` | 可选字符串，默认空 | 需要屏蔽的站点列表（逗号分隔）。 |
| `WHOOGLE_CONFIG_SAFE` | 枚举（0/1），默认空 | 是否启用安全搜索。 |
| `WHOOGLE_CONFIG_ALTS` | 枚举（0/1），默认空 | 是否使用替代前端（alternative frontends）。 |
| `WHOOGLE_CONFIG_NEW_TAB` | 枚举（0/1），默认空 | 是否在新标签页中打开搜索结果。 |
| `WHOOGLE_CONFIG_VIEW_IMAGE` | 枚举（0/1），默认空 | 是否启用「查看图片」选项。 |
| `WHOOGLE_CONFIG_GET_ONLY` | 枚举（0/1），默认空 | 是否仅使用 GET 请求。 |
| `WHOOGLE_CONFIG_DISABLE` | 枚举（0/1），默认空 | 是否禁止用户在界面上修改设置。 |
| `WHOOGLE_AUTOCOMPLETE` | 枚举（0/1），默认空 | 是否启用搜索自动补全。 |
| `WHOOGLE_MINIMAL` | 枚举（0/1），默认空 | 是否启用极简模式。 |
| `WHOOGLE_CSP` | 枚举（0/1），默认空 | 是否启用内容安全策略（CSP）。 |
| `HTTPS_ONLY` | 枚举（0/1），默认空 | 是否仅通过 HTTPS 访问。 |
| `WHOOGLE_RESULTS_PER_PAGE` | 整数（5–100），默认空 | 每页显示的结果条数。 |
| `WHOOGLE_USER` | 可选字符串，默认空 | 认证用户名。 |
| `WHOOGLE_PASS` | 可选密码，默认空 | 认证密码。 |
| `WHOOGLE_PROXY_TYPE` | 可选字符串，默认空 | 代理类型。 |
| `WHOOGLE_PROXY_LOC` | 可选字符串，默认空 | 代理位置。 |
| `WHOOGLE_PROXY_USER` | 可选字符串，默认空 | 代理用户名。 |
| `WHOOGLE_PROXY_PASS` | 可选字符串，默认空 | 代理密码。 |
| `WHOOGLE_ALT_TW` | 可选字符串，默认空 | Twitter 的替代前端地址。 |
| `WHOOGLE_ALT_YT` | 可选字符串，默认空 | YouTube 的替代前端地址。 |
| `WHOOGLE_ALT_IG` | 可选字符串，默认空 | Instagram 的替代前端地址。 |
| `WHOOGLE_ALT_RD` | 可选字符串，默认空 | Reddit 的替代前端地址。 |
| `WHOOGLE_ALT_MD` | 可选字符串，默认空 | Medium 的替代前端地址。 |
| `WHOOGLE_ALT_TL` | 可选字符串，默认空 | TikTok 的替代前端地址。 |

## 使用 / 访问入口

- 加载项支持 Ingress，启动后可在 Home Assistant 侧边栏看到 Whoogle Search 图标，点击进入。
- Web 界面容器端口 `5000/tcp`，宿主端口 5000（如需直接访问，可在加载项端口设置中开启）。

## 常见问题

- **如何设置访问密码？** 通过 `WHOOGLE_USER` 与 `WHOOGLE_PASS` 配置认证用户名与密码即可。
- **如何屏蔽某些网站？** 在 `WHOOGLE_CONFIG_BLOCK` 中填写要屏蔽的站点域名，多个用逗号分隔。
- **如何自定义界面？** 可通过 `WHOOGLE_CONFIG_THEME`（主题）、`WHOOGLE_CONFIG_LANGUAGE`（界面语言）等选项调整，也可在 Web 界面中直接修改。
- **完整的可选环境变量说明？** 参见上游 benbusby/whoogle-search 的「Environment variables」文档。
- **需要自定义环境变量？** 通过 `env_vars` 选项传入（变量名支持大小写），参见上游 wiki「Add environment variables to your add-on」。
- 自 0.9.4-2 起，数据与配置迁移到 `/addon_configs/db21ed7f_whoogle_search`，可随加载项一起备份；自 0.7.1 起配置处理方式有重大变更，旧配置需要重新设置。

---
- 英文原版：Home assistant add-on: whoogle-search；链接 https://github.com/alexbelgium/hassio-addons/blob/master/whoogle/README.md
- 来源仓库：alexbelgium
