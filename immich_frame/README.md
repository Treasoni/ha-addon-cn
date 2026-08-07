<!-- zh-guide -->
# Immich Frame

## 简介
Immich Frame 将你的 Immich 图库展示为数字相框：把任何屏幕变成精美的个人照片与回忆轮播展示，非常适合把闲置的旧平板或显示器改造成专属照片展示设备。本加载项可连接你的 Immich 服务器，以幻灯片形式展示照片，支持单账户与多账户模式。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 immich_frame 并安装。

## 配置
除下表列出的选项外，其余显示设置可在 Web 界面中调整。使用多账户时，请在 `Accounts` 列表中填写各账户信息，此时顶层 `ImmichServerUrl` 与 `ApiKey` 不再需要。

| 配置键 | 类型 / 默认值 | 说明 |
|--------|--------------|------|
| `ImmichServerUrl` | 字符串（可选） | Immich 服务器地址，用于单账户配置（如 `homeassistant:3001`） |
| `ApiKey` | 字符串（可选） | Immich API 密钥，用于单账户配置 |
| `TZ` | 字符串（可选） | 时区，如 `Europe/London`、`Asia/Shanghai` |
| `Accounts` | 列表 / 默认 `[]` | Immich 账户列表，用于多账户展示；每个条目需 `ImmichServerUrl` 与 `ApiKey`，并可设置相册、人物、标签、收藏、视频等筛选字段 |
| `env_vars` | 列表 / 默认 `[]` | 额外传给 ImmichFrame 的环境变量（键名需匹配 `^[A-Za-z0-9_]+$`），会被自动归类为通用或账户级设置并写入 Settings.yaml |
| `Interval` | 整数（可选） | 图片切换间隔（秒），默认 45 秒 |
| `TransitionDuration` | 浮点（可选） | 切换过渡时长（秒），默认 2 秒 |
| `ShowClock` | 布尔（可选） | 是否显示当前时间，默认开启 |
| `ClockFormat` | 字符串（可选） | 时钟时间格式，默认 `hh:mm` |
| `ClockDateFormat` | 字符串（可选） | 时钟日期格式，默认 `eee, MMM d` |
| `ShowProgressBar` | 布尔（可选） | 是否显示进度条，默认开启 |
| `ShowPhotoDate` | 布尔（可选） | 是否显示当前照片的日期，默认开启 |
| `PhotoDateFormat` | 字符串（可选） | 照片日期格式，默认 `MM/dd/yyyy` |
| `ShowImageDesc` | 布尔（可选） | 是否显示图片描述，默认开启 |
| `ShowPeopleDesc` | 布尔（可选） | 是否显示人物名称，默认开启 |
| `ShowTagsDesc` | 布尔（可选） | 是否显示标签名称，默认开启 |
| `ShowAlbumName` | 布尔（可选） | 是否显示相册名称，默认开启 |
| `ShowImageLocation` | 布尔（可选） | 是否显示拍摄地点，默认开启 |
| `ShowWeatherDescription` | 布尔（可选） | 是否显示天气描述，默认开启 |
| `ImageZoom` | 布尔（可选） | 是否对图片做轻微缩放，默认开启 |
| `ImagePan` | 布尔（可选） | 是否沿随机方向平移图片，默认关闭 |
| `ImageFill` | 布尔（可选） | 是否填满可用空间（可能裁切），默认关闭 |
| `PlayAudio` | 布尔（可选） | 是否播放带音轨视频的音频，默认关闭 |
| `PrimaryColor` | 字符串（可选） | 主要界面颜色（十六进制），默认 `#f5deb3` |
| `SecondaryColor` | 字符串（可选） | 次要界面颜色（十六进制），默认 `#000000` |
| `Style` | 字符串（可选） | 背景样式：`none`、`solid`、`transition`、`blur` |
| `Layout` | 字符串（可选） | 布局：`single` 或 `splitview` |
| `BaseFontSize` | 字符串（可选） | 基础字号（CSS 格式），默认 `17px` |
| `Language` | 字符串（可选） | 两位 ISO 语言代码，默认 `en` |
| `WeatherApiKey` | 字符串（可选） | OpenWeatherMap API 密钥 |
| `UnitSystem` | 字符串（可选） | 单位制：`imperial` 或 `metric`，默认 `imperial` |
| `WeatherLatLong` | 字符串（可选） | 天气位置，格式 `lat,lon` |
| `ImageLocationFormat` | 字符串（可选） | 位置显示格式，默认 `City,State,Country` |
| `DownloadImages` | 布尔（可选） | 是否将图片下载到服务器，默认关闭 |
| `RenewImagesDuration` | 整数（可选） | 多少天后重新下载图片，默认 30 天 |
| `RefreshAlbumPeopleInterval` | 整数（可选） | 相册/人物刷新间隔（小时），默认 12 小时 |

## 使用 / 访问入口
- 启动后通过浏览器访问宿主端口 8171 打开 Web 界面（对应容器端口 8080）。
- 首次使用前，需在配置中填写 Immich 服务器地址与 API 密钥（Immich → Administration → API Keys → Create API Key 获取）。

## 常见问题
- **如何获取 Immich API 密钥？** 打开 Immich Web 界面，进入 Administration → API Keys，创建 API 密钥并复制。
- **多账户怎么配置？** 在 `Accounts` 列表中为每个账户填写 `ImmichServerUrl` 与 `ApiKey`，并可添加相册、人物、标签等筛选；此时顶层 `ApiKey` 与 `ImmichServerUrl` 可留空，图片会按各账户图片总数比例轮播。
- **界面显示不理想？** 可通过 `Layout`、`Style`、`PrimaryColor` 等选项调整布局与配色，并在 Web 界面中进一步微调。

---
- 英文原版：[Home assistant add-on: Immich Frame](https://github.com/alexbelgium/hassio-addons/blob/master/immich_frame/README.md)
- 来源仓库：alexbelgium
