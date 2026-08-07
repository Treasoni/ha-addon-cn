<!-- zh-guide -->
# Tautulli

## 简介

Tautulli 是一款与 Plex Media Server 搭配使用的监控与统计工具。它运行在你的 Plex 媒体服务器旁，记录什么内容被观看、谁观看的、在何时何地以及通过什么方式观看，并以表格和图表的清晰界面呈现这些数据，方便你了解媒体库的使用情况。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 tautulli 并安装。
3. 安装后启动加载项，首次启动可能需要几分钟，请耐心等待。

## 配置

| 配置键 | 类型/默认值 | 说明 |
|--------|------------|------|
| `log_level` | 枚举（trace/debug/info/notice/warning/error/fatal），默认 `info` | 控制加载项日志输出的详细程度。级别越高越详细：`trace` 显示所有内部调用细节，`debug` 显示调试信息，`info` 为常规事件，`warning` 为非错误的异常情况，`error` 为无需立即处理的运行时错误，`fatal` 表示加载项已不可用的严重错误。排障时可调低以获取更多信息，日常使用保持 `info` 即可。 |

> 提示：修改配置后需要重启加载项才能生效。

## 使用 / 访问入口

- **Web 界面**：加载项提供 Web 界面，默认端口 `8181/tcp`（映射到主机 `8181` 端口）。
- **首次访问**：启动加载项后，点击加载项页面上的「打开 Web UI」，按首次配置向导完成设置即可使用。
- **常用操作**：在界面中查看实时播放活动，以及观看历史、观看者、观看时间与方式等统计数据。
- **嵌入 Home Assistant**：可使用 `panel_iframe` 集成把 Tautulli 嵌入 HA 前端，例如：
  ```yaml
  panel_iframe:
    tautulli:
      title: Tautulli
      icon: mdi:filmstrip
      url: http://你的HomeAssistant地址:8181
  ```

## 常见问题

- **首次启动很慢或界面迟迟打不开？** 首次启动（尤其是刚安装后）可能需要几分钟，请耐心等待，并查看加载项「日志」确认是否启动正常。
- **改了配置不生效？** 修改任何配置后都需要重启加载项才会生效。
- **找不到访问入口？** 安装并启动加载项后，在加载项页面点击「打开 Web UI」，然后按首次向导完成初始化。

---
- 英文原版：Home Assistant Community Add-on: Tautulli；链接 https://github.com/hassio-addons/repository/blob/master/tautulli/README.md
- 来源仓库：frenck
