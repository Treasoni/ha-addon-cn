# 铁律

从 `LEARNINGS.md` 和 `ERRORS.md` 提炼出的最高优先级规则。

---

_最后更新：2026-08-07_

## 镜像源验证（registry proxy）

- **验证镜像源**：用 `GET /v2/<repo>/manifests/<真实version>` 探测，2xx 才可用；勿用 `tags/list`（pull-through 代理对未缓存仓库返回假 NAME_UNKNOWN）、勿用 `latest`（frenck/官方无此 tag）。

## 同步覆盖文件的系统改写

- **对同步会覆盖的文件做系统改写**：做成同步管道里的幂等变换（拷贝后改写、改写后再对比），勿原地手工改，否则下次同步被冲掉且脏目录阻塞同步。

## 脚本输出编码

- **CLI 脚本输出**：统一 `sys.stdout.reconfigure(encoding="utf-8")`，避免 Windows 管道/控制台中文乱码或 grep 失配。

## 环境判断

- **GitHub 网络**：国内访问 GitHub 会抖动（fetch 失败 ≠ push 失败），网络类报错先重试/稍后再跑，别急着改脚本。
- **工作区状态**：操作前自己跑 `git status --short` 自证，勿依赖会话开始时的 status 快照。
