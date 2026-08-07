<!-- zh-guide -->
# motionEye

## 简介

motionEye 是一款简单、优雅且功能丰富的开源 CCTV/NVR 摄像头监控软件，也是知名相机软件 motion 的前端界面。本加载项将两者打包，让你能轻松把摄像头接入 Home Assistant。它可用于婴儿监控、工地画面查看、商店 DVR、庭院安防等众多场景。

主要特性：

- 支持海量摄像头，包括 IP 摄像头。
- 可接入多台 motionEye 实例实现多摄像头联动（例如局域网内的 MotionEyeOS + Pi 摄像头）。
- 支持将录像上传至 Google Drive 和 Dropbox。
- 支持运动检测，含邮件通知与定时调度。
- 支持连续录像、运动触发录像或延时摄影，并可配置保留时长。

## 安装

1. 在 Home Assistant 中进入「设置 → 加载项 → 商店」，点击右上角菜单添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 在商店中搜索 `motioneye`（motionEye）并点击安装。
3. 启动加载项并在日志中确认一切正常，然后打开 Web 界面。
4. 首次登录使用用户名 `admin`、无需密码；登录后请务必为管理员账号设置安全密码。

## 配置

> 注意：修改配置后需重启加载项才会生效。

| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `log_level` | 枚举（trace\|debug\|info\|notice\|warning\|error\|fatal），可选 / 空 | 加载项的日志输出级别。`trace` 显示全部细节，`debug` 显示详细调试信息，`info` 为正常事件，`warning` 为非错误的异常，`error` 为无需立即处理的错误，`fatal` 为致命错误。推荐使用 `info`。 |
| `motion_webcontrol` | 布尔 / false | 是否在 7999 端口启用 motion webcontrol 端点。注意：该端点不支持认证、也不支持 SSL，仅在完全了解风险时启用，绝不要将其暴露到外网。 |
| `ssl` | 布尔 / true | 是否在 motionEye Web 界面启用 SSL（HTTPS）。设为 `true` 启用，`false` 禁用。 |
| `certfile` | 字符串 / fullchain.pem | 用于 SSL 的证书文件，必须存放在 `/ssl/` 目录下。 |
| `keyfile` | 字符串 / privkey.pem | 用于 SSL 的私钥文件，必须存放在 `/ssl/` 目录下。 |
| `action_buttons` | 列表（对象列表） / 空 | 动作按钮列表。配置后将为每个按钮创建对应脚本，在 motionEye 界面中显示可点击的操作按钮。 |
| `action_buttons.type` | 枚举（lock\|unlock\|light_on\|light_off\|alarm_on\|alarm_off\|up\|right\|down\|left\|zoom_in\|zoom_out\|preset1–preset9），可选 / 空 | 动作按钮类型，例如上锁/解锁、开灯/关灯、报警开/关、云台方向、缩放、预设位等。 |
| `action_buttons.camera` | 整数，可选 / 空 | 目标摄像头编号，对应 motionEye 界面中设置的摄像头编号。 |
| `action_buttons.command` | 字符串，可选 / 空 | 按下按钮时执行的 bash 命令。 |

## 使用 / 访问入口

启动后可在 Home Assistant 侧边栏看到 motionEye 图标，点击进入即可打开 Web 界面。

## 常见问题

- **首次登录账号**：默认用户名为 `admin`，密码为空，登录后应立即设置一个安全密码。
- **`motion_webcontrol` 安全提示**：该端点不支持认证与 SSL，启用后请不要将其端口暴露到公网。
- **SSL 与侧边栏访问**：SSL 设置只作用于直接端口访问，对 Ingress（侧边栏）访问不生效，属正常现象。
- **日志过多或过少**：可通过 `log_level` 调整日志详细程度，排查问题时临时调低级别，问题解决后改回 `info`。

---
- 英文原版：motionEye；链接 https://github.com/hassio-addons/repository/blob/main/motioneye/README.md
- 来源仓库：frenck
