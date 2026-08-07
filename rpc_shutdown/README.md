<!-- zh-guide -->
# RPC Shutdown

## 简介
本加载项通过 RPC 远程关闭 Windows 电脑。你可以在 Home Assistant 中通过服务调用，远程安全地关闭一台或多台 Windows 机器。

## 安装
1. 在 Home Assistant → 设置 → 加载项 → 商店，添加本商店仓库：
   - Gitee：https://gitee.com/zhqznc_10603234_123/ha-addon
   - GitHub：https://github.com/Treasoni/ha-addon-cn
2. 搜索 rpc_shutdown 并安装。

## 配置
| 配置键 | 类型 / 默认值 | 说明 |
| --- | --- | --- |
| `computers` | 列表 / 默认包含一条示例 | 需要远程关闭的 Windows 电脑列表，每台电脑一条记录 |
| `computers.address` | 字符串 | 电脑的 IP 地址或 NetBIOS 名称（必填） |
| `computers.alias` | 字符串（字母、数字、`_`、`-`） | 本条记录的别名，将作为 Home Assistant 服务调用的 `input` 参数 |
| `computers.credentials` | 字符串 | 登录凭据，用户名与密码之间用 `%` 分隔，如 `user%password` |
| `computers.delay` | 整数（0–600）/ 空 | 关机前的延迟秒数，给正在使用该电脑的人保存工作的时间 |
| `computers.message` | 字符串 / 空 | 关机前在电脑屏幕上显示的提示消息 |

## 使用 / 访问入口
该加载项没有 Web 界面，也没有对外端口。配置完成后启动加载项，然后在 Home Assistant 中调用服务 `hassio.app_stdin`：
- `app`：`core_rpc_shutdown`
- `input`：配置中某台电脑的 `alias` 别名

即可远程关闭对应电脑，结果可查看加载项日志。

## 常见问题
- **凭据格式**：`credentials` 使用 `%` 分隔用户名和密码（如 `user%password`）；密码本身也可以包含 `%`。
- **延迟与消息**：`delay`（秒）与 `message`（屏幕提示）均为可选；`delay` 留空时按 `0` 处理。
- **目标电脑设置**：目标 Windows 电脑需要具备允许远程关机（RPC）的相关配置。

---
- 英文原版：Home Assistant App: RPC Shutdown（[链接](https://github.com/home-assistant/addons/blob/master/rpc_shutdown/README.md)）
- 来源仓库：official
