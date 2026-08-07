<!-- zh-guide -->
# Grocy

## 简介

Grocy 是一款功能强大的食品杂货与家庭管理解决方案（“超出冰箱的 ERP”），为家庭场景提供了库存管理、购物清单、菜谱、杂务与任务、盘点等功能。通过本加载项，你可以直接在 Home Assistant 中管理家庭的库存与日常事务。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 grocy 并安装。

## 配置

在加载项“配置”页修改配置后，需要重启加载项才能生效。可选配置键如下：

| 配置键 | 类型/默认值 | 说明 |
| ------ | ----------- | ---- |
| `log_level` | 可选 `list(trace|debug|info|notice|warning|error|fatal)`，默认 `info` | 日志输出详细程度：`trace` 输出全部细节；`debug` 输出调试信息；`info` 常规事件；`warning` 非错误的异常事件；`error` 运行时错误；`fatal` 致命错误。更高级别会自动包含更低级别的日志，默认 `info` 是推荐设置 |
| `ssl` | `bool`，默认 `true` | 是否在 Grocy Web 界面启用 SSL（HTTPS），设为 `true` 启用 |
| `certfile` | `str`，默认 `fullchain.pem` | 用于 SSL 的证书文件，必须存放在 `/ssl/` 目录 |
| `keyfile` | `str`，默认 `privkey.pem` | 用于 SSL 的私钥文件，必须存放在 `/ssl/` 目录 |
| `culture` | 枚举 `list(ca|cs|da|de|el_GR|en|en_GB|es|et|fi|fr|he_IL|hu|it|ja|ko_KR|lt|nl|no|pl|pt_BR|pt_PT|ro|ru|sk_SK|sl|sv_SE|ta|tr|uk|zh_CN|zh_TW)`，默认 `en` | 设置界面语言，例如 `en`（英语）、`zh_CN`（简体中文）、`zh_TW`（繁体中文） |
| `currency` | `str`，默认 `USD` | 界面中显示的货币，采用 ISO4217 三位货币代码，例如 `USD`、`CAD`、`GBP` 或 `EUR` |
| `entry_page` | 枚举 `list(stock|shoppinglist|recipes|chores|tasks|batteries|equipment|calendar|mealplan)`，默认 `stock` | 自定义主页，可选 `stock`、`shoppinglist`、`recipes`、`chores`、`tasks`、`batteries`、`equipment`、`calendar`、`mealplan`；默认主页为库存总览 |
| `grocycode_type` | 枚举 `list(1D|2D)`，默认 `2D` | 更改 GrocyCode 的条形码类型，`1D`（Code128）或 `2D`（DataMatrix），适用于条形码扫描器不支持默认类型的情况 |
| `features` | 对象/嵌套配置，默认 `空` | 启用或禁用 Grocy 的功能模块，被禁用的功能将从界面中隐藏（见下方子键） |
| `features.batteries` | `bool`，默认 `true` | 是否启用「电池」功能 |
| `features.calendar` | `bool`，默认 `true` | 是否启用「日历」功能 |
| `features.chores` | `bool`，默认 `true` | 是否启用「杂务」功能 |
| `features.equipment` | `bool`，默认 `true` | 是否启用「设备」功能 |
| `features.recipes` | `bool`，默认 `true` | 是否启用「菜谱」功能 |
| `features.shoppinglist` | `bool`，默认 `true` | 是否启用「购物清单」功能 |
| `features.stock` | `bool`，默认 `true` | 是否启用「库存」功能 |
| `features.tasks` | `bool`，默认 `true` | 是否启用「任务」功能 |
| `printers` | 对象/嵌套配置，默认 `空` | 配置标签打印机与热敏打印机支持（见下方子键） |
| `printers.label_printer` | 对象/嵌套配置，默认 `空` | 标签打印机配置，通过 webhook 打印标签 |
| `printers.label_printer.enabled` | `bool`，默认 `false` | 设为 `true` 启用通过 webhook 打印标签 |
| `printers.label_printer.webhook` | 可选 `str`，默认 `空` | 打印标签时 Grocy 向其 POST 请求的 URI |
| `printers.label_printer.run_server` | 可选 `bool`，默认 `空` | 设为 `false` 时改为在客户端调用 webhook，而非服务器端调用 |
| `printers.label_printer.params` | 可选 `str`，默认 `空` | 提供给 webhook 的附加参数 |
| `printers.label_printer.hook_json` | 可选 `bool`，默认 `空` | 设为 `true` 以 JSON 形式 POST，`false` 使用普通表单编码变量 |
| `printers.thermal_printer` | 对象/嵌套配置，默认 `空` | 热敏打印机配置（支持 ESC/POS 协议，仅支持网络打印机） |
| `printers.thermal_printer.enabled` | `bool`，默认 `false` | 设为 `true` 启用热敏打印 |
| `printers.thermal_printer.ip` | 可选 `str`，默认 `空` | 网络打印机的 IP 地址 |
| `printers.thermal_printer.port` | 可选 `int`，默认 `空` | 网络打印机的端口 |
| `printers.thermal_printer.print_quantity_name` | 可选 `bool`，默认 `空` | 设为 `false` 在打印输出中省略数量名称 |
| `printers.thermal_printer.print_notes` | 可选 `bool`，默认 `空` | 设为 `false` 在打印输出中省略备注 |
| `tweaks` | 对象/嵌套配置，默认 `空` | 微调 Grocy 的部分核心行为（见下方子键） |
| `tweaks.chores_assignment` | `bool`，默认 `true` | 是否启用「杂务分配」微调 |
| `tweaks.multiple_shopping_lists` | `bool`，默认 `true` | 是否启用「多购物清单」微调 |
| `tweaks.stock_best_before_date_tracking` | `bool`，默认 `true` | 是否启用「库存保质期追踪」微调 |
| `tweaks.stock_location_tracking` | `bool`，默认 `true` | 是否启用「库存位置追踪」微调 |
| `tweaks.stock_price_tracking` | `bool`，默认 `true` | 是否启用「库存价格追踪」微调 |
| `tweaks.stock_product_freezing` | `bool`，默认 `true` | 是否启用「库存产品冷冻」微调 |
| `tweaks.stock_product_opened_tracking` | `bool`，默认 `true` | 是否启用「库存开封产品追踪」微调 |
| `tweaks.stock_count_opened_products_against_minimum_stock_amount` | `bool`，默认 `true` | 是否将开封产品计入最低库存量统计的微调 |
| `tweaks.calendar_first_day_of_week` | 可选 `int`，默认 `空` | 日历一周的起始日（0-6，其中 0 为周日） |
| `tweaks.meal_plan_first_day_of_week` | 可选 `int`，默认 `空` | 膳食计划一周的起始日（0-6，其中 0 为周日） |
| `grocy_ingress_user` | `str`，默认 `空` | 指定 Ingress 访问的默认用户（如 `admin`）；未设置时使用默认登录认证 |

## 使用 / 访问入口

- **Web 界面**：加载项支持 Ingress，启动后可在 Home Assistant 侧边栏看到 Grocy 图标，点击进入。
- **默认登录**：默认账号为 `admin`，密码为 `admin`。
- **直接访问（可选）**：端口 `80/tcp` 为直连端口（Ingress 场景下无需使用），仅在需要绕过 Ingress 直接访问时才会用到。

## 常见问题

- **条形码扫描器无法使用？** Grocy 的条形码扫描功能需要浏览器摄像头权限，而浏览器仅在安全上下文（HTTPS 或 localhost）下允许摄像头访问。若通过 HTTP 的 Ingress 面板访问，浏览器会拒绝摄像头。如需使用扫码功能，请启用 SSL 并通过端口直接访问 Grocy。
- **如何切换中文界面？** 将 `culture` 设为 `zh_CN`（简体中文）或 `zh_TW`（繁体中文），保存并重启加载项即可。
- **扫描产品条码的联网查询不可用？** Grocy 基于产品条码在互联网上查询信息的自定义查找资源功能，目前本加载项暂不支持。
- **标签打印机打印异常？** 请确认 `printers.label_printer` 的 `webhook` 地址正确，并按需设置 `hook_json` 与 `params`；热敏打印机仅支持网络打印机（不支持 USB/串口直连）。

---
- 英文原版：Home Assistant Community App: Grocy；链接 https://github.com/hassio-addons/repository/blob/main/grocy/README.md
- 来源仓库：frenck
