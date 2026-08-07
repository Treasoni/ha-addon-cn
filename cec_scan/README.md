<!-- zh-guide -->
# CEC Scanner

## 简介
本加载项用于扫描并发现 HDMI CEC 设备及其 CEC 地址。它可以帮助你查看电视、机顶盒、播放器等通过 HDMI 连接的设备所使用的 CEC 地址，方便你配置与调试 CEC 控制。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 cec_scan 并安装。

## 配置
该加载项没有可配置项（`options` 与 `schema` 均为空），无需额外配置。

## 使用 / 访问入口
该加载项没有 Web 界面，也没有对外端口。它属于「运行一次」类型：手动点击「启动」后进行一次 HDMI CEC 扫描，检测到的设备及其 CEC 地址会输出到加载项的日志中。

## 常见问题
- **Raspberry Pi 上提示 autodetect FAILED**：这是旧版本在树莓派上偶发的已知问题，已在 v2.2 中修复，请升级到最新版本。
- **支持的 CEC 实现**：加载项支持 Meson AOCEC、Exynos 以及 Linux 原生 CEC，可覆盖多数常见主板与树莓派。
- **架构支持**：自 v4.0 起仅支持 aarch64 与 amd64 架构。

---
- 英文原版：Home Assistant App: CEC Scanner（[链接](https://github.com/home-assistant/addons/blob/master/cec_scan/README.md)）
- 来源仓库：official
