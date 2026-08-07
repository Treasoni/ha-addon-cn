<!-- zh-guide -->
# VLC

## 简介
本加载项基于 VLC，将运行它的设备变成一个媒体播放器（Media Player），供 Home Assistant 调用播放本地媒体（如共享中的音乐、视频）。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 vlc 并安装。

## 配置
该加载项没有可配置项（`options` 为空，`schema` 为 `false`），无需额外配置。

## 使用 / 访问入口
启动后可在 Home Assistant 侧边栏看到 VLC 图标，点击进入。加载项通过 VLC telnet 接口被发现，Home Assistant 的 VLC 集成会自动配置媒体播放器。

## 常见问题
- **媒体来源**：加载项可以访问 Home Assistant 的共享（share）与媒体（media）目录中的文件。
- **音频插件重启**：音频插件重启时加载项会自动重启 VLC，以保持媒体播放器可用。
- **无配置项**：该加载项无需额外配置即可使用。

---
- 英文原版：Home Assistant App: VLC（[链接](https://github.com/home-assistant/addons/blob/master/vlc/README.md)）
- 来源仓库：official
