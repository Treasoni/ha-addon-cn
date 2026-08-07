<!-- zh-guide -->
# HACS极速版安装器

## 简介

HACS极速版安装器（slug：`get`）是**最简单的 HACS 极速版安装方式**：一键把 HACS 极速版或常用国内集成安装进 Home Assistant，无需手动下载、解压、拷贝文件。除了 HACS，它还能安装 xiaomi_miot、edge_tts、sonoff 等常用集成。

> 此加载项可以安装 HACS 极速版及部分常用集成。

## 安装

1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索「HACS极速版安装器」（slug：`get`）并安装。
3. 安装前可先在「配置」页选好要安装的组件与渠道（见下）。

## 配置

此加载项为**一次性安装器**，安装目标写在配置里，启动后按配置执行：

| 配置键 | 类型/默认值 | 说明 |
| ------ | ----------- | ---- |
| `component` | 枚举，默认 `hacs` | 要安装的组件（集成）：`hacs`（HACS 极速版）、`xiaomi_miot`、`xiaomi_home`、`xiaomi_gateway3`、`sonoff`、`tianqi`、`edge_tts`、`yeelight_pro`、`ai_conversation`、`ha_file_explorer`、`bemfa`、`midea_ac_lan`、`haier`、`terncy` |
| `channel` | 可选枚举，默认 `current` | 安装渠道：`current`（正式版，推荐）或 `development`（开发版） |

## 使用方法

1. 在「配置」页选择要安装的组件（默认 HACS）和渠道，点击「保存」。
2. 点击「安装」构建此加载项。
3. 点击「启动」运行一次（此加载项 `startup: once`，运行完即自动退出，不会常驻）。
4. 切换到「日志」页，按日志提示等待下载与安装完成。
5. 安装完成后**重启 Home Assistant**，然后到 设置 → 设备与服务 → 添加集成，搜索并添加刚安装的集成。

![操作步骤](https://github.com/user-attachments/assets/89fb128c-6cff-49aa-8faa-3a56bca078f7)

> 安装器会把组件写入 Home Assistant 配置目录的 `custom_components/` 下，若该目录不存在会自动创建。

## 常见问题

- **启动后很快就退出了，是坏了吗？** 不是。这是**一次性安装器**（`startup: once` + `boot: manual`），启动执行完安装就会退出，这是设计行为；安装结果请看「日志」页。
- **安装完 HACS 后商店里看不到？** 请重启 Home Assistant，然后在 设置 → 设备与服务 → 添加集成 中搜索「HACS」并添加。
- **想安装其他集成怎么办？** 在「配置」页把 `component` 改为目标组件（如 `xiaomi_miot`、`edge_tts`），再启动一次即可。
- **`channel` 是什么？** `channel` 是安装渠道，可选 `current`（正式版，默认）或 `development`（开发版），一般保持默认 `current` 即可；实际安装行为以加载项「日志」页为准。
- **下载失败或很慢？** 此加载项由国内社区（hacs-china）维护，下载走极速版脚本，相对官方更稳定；偶发失败可重试启动。

---
- 英文原版：[HACS极速版安装器 README](https://gitee.com/hacs-china/addons/raw/china/get/README.md)
- 来源仓库：hacs-china
