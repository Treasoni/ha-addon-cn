# HAOS 镜像检查工具默认只读

Status: accepted

## 背景

旧版本通过 `docker cp` 修改 `hassio_supervisor:/data/docker.json` 的
`registries_mirror` 字段，并重启 Supervisor。该字段不是当前 Supervisor
公开支持的配置接口，也不会可靠地改变 HAOS Docker daemon 对 GHCR、Docker
Hub 或 LSCR 的实际拉取路径。实际表现是页面显示应用成功，但安装加载项仍
然等待境外 registry；自动自愈还可能在每次启动时重复写入。

## 决策

- `probe_all` 和自动周期任务只执行真实 manifest 检查并记录结果。
- `apply` 和 `restore_backup` 永久拒绝写入 Supervisor 镜像配置，并返回
  `MIRROR_APPLICATION_UNSUPPORTED`。
- Web 界面停用“应用推荐配置”和“恢复上次配置”，避免小白用户误以为
  检查结果已经改变了 Supervisor 的拉取路径。
- 保留“清除旧配置并恢复直连”作为一次性的兼容救援入口。它只在用户明确
  点击后删除旧版留下的 `registries_mirror` 字段，清空本地旧快照，并在
  成功后重启 Supervisor。
- 国内关键路径依靠预构建 add-on 镜像入口和真实可拉取的镜像地址；不能用
  一个未经验证的内部 JSON 字段替代 HAOS 官方 Docker 配置机制。

## 后果

本加载项不再承诺“运行时一键切换所有 registry”。用户如果要长期配置
Docker Hub mirror，必须使用目标 HAOS 版本实际支持的系统级方案；GHCR 和
LSCR 仍需使用真实的 image host 重写或可验证的 registry proxy。这个边界
优先保证安装失败时不会继续破坏 Supervisor 状态。
