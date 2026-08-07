<!-- zh-guide -->
# Folding@home

## 简介

Folding@home（FAH 或 F@h）是一个分布式计算项目，用于进行蛋白质动力学的分子动力学模拟。它最初聚焦于蛋白质折叠，如今已扩展到更多生物医学问题，例如阿尔茨海默病、癌症、埃博拉和冠状病毒。该项目使用志愿者电脑的闲置计算资源来参与计算。通过本加载项，你可以将 Home Assistant 设备的空闲时间捐献给 Folding@home 项目，帮助抗击这些疾病。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 foldingathome 并安装。

## 配置

本加载项在加载项“配置”页中没有任何可配置的选项（config.yaml 未定义 options/schema）。Folding@home 的运行设置（如用户名、团队、运行模式等）都可以通过其 Web 界面进行管理。默认情况下，加载项会自动加入 Home Assistant 团队（团队编号：247478）。

## 使用 / 访问入口

- **Web 界面**：加载项将端口 `7396/tcp` 映射到宿主机端口 7396，启动后在浏览器地址栏输入你的设备 IP 与端口 7396 即可打开 Folding@home 的 Web 界面。
- **远程命令接口**：端口 `36330/tcp` 为远程命令接口，未映射到宿主机端口，仅供高级用户使用。
- **团队统计**：可访问 Folding@home 团队统计页面（https://stats.foldingathome.org/team/247478）查看 Home Assistant 团队的贡献情况。

## 常见问题

- **加入哪个团队？** 默认加入 Home Assistant 团队（id: 247478），你也可以在 Web 界面中修改团队设置。
- **会不会影响 Home Assistant 正常运行？** 加载项使用设备的闲置计算资源进行蛋白质模拟，会占用部分 CPU 资源，请在资源充足的设备上使用。
- **哪些设备可以安装？** 本加载项仅支持 amd64 架构的设备。

---
- 英文原版：Home Assistant Community Add-on: Folding@home；链接 https://github.com/hassio-addons/repository/blob/main/foldingathome/README.md
- 来源仓库：frenck
