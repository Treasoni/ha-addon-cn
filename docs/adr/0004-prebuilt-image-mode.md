# 自有 add-on 支持「预构建模式」（source: local + 预构建镜像）

`source: local` 自有 add-on 默认由 Supervisor 本地构建；当本地构建需要拉取国内不可达的中间镜像时，允许 add-on 进入**预构建模式**——config.yaml 声明 `image:` 指向 CI 构建推送的镜像，Supervisor 只拉取、不本地构建。本 ADR 记录这一例外及其判定。

Status: accepted

**问题**：`source: local` 自有 add-on 默认由 Supervisor 本地构建，装前需同时拉两条通道：Docker Hub 构建器 CLI 镜像（`docker:*`，仓库 `library/docker`，走 docker.io 通道）与 ghcr.io `{arch}-base` 基础镜像（走 ghcr 通道）。国内网络下两条必须都先可用才能安装——鸡生蛋：新手要先手动配好两个 `registries_mirror` 映射才能装，装完 add-on 才接管换源。`haos-mirror-switcher` 真机实测拉 Docker Hub 构建器 CLI 即报 `Can't pull image docker:29.6.2-cli` / `auth.docker.io ... EOF`。

**决策**：允许 `source: local` 的 add-on 进入「预构建模式（prebuilt mode）」：
- config.yaml 上游资料卡加 `# prebuilt: true` 注释，并写 `image: ghcr.nju.edu.cn/<owner>/<slug>-{arch}`（`-{arch}` 后缀形态，check-docker D08 校验）。
- 镜像由新增工作流 `.github/workflows/build-addon.yml`（buildx 矩阵：amd64 + aarch64）构建推送 ghcr.io，再由国内 pull-through 入口提供安装；Supervisor 安装时只拉取、不本地构建。
- 安装只需国内预构建入口单通道，不再要求用户先打通 Docker Hub/GHCR 双通道，也不再需要 Docker Hub 构建器 CLI 镜像。
- 门禁同步放宽：check-addon C9 仅在有 `image:` 而无 `# prebuilt: true` 时 FAIL（并有 W3 反向警告：声明 prebuilt 却缺 image）；check-docker D08 校验 `image:` 的 `{arch}` 形态。

**验证方法**：`check-addon.py haos-mirror-switcher` PASS；`check-docker.sh --path haos-mirror-switcher` D08 通过且 addon-7 不触发（config.yaml 无 `source:` 字段）；workflow_dispatch 构建后 `docker manifest inspect ghcr.io/treasoni/haos-mirror-switcher-amd64:0.1.0` 可验证镜像存在。

**Considered Options**：
- 保持纯本地构建——装前双通道鸡生蛋无解（正是本 ADR 要解决的），放弃。
- `image:` 保持 ghcr.io 规范形态、依赖宿主 `registries_mirror` 单映射——仍要求用户先配置镜像源，无法解决首次安装的鸡生蛋问题，放弃。
- 同时推 arch-less manifest list 镜像——Dockerfile 按 arch 用不同 `build_from`，单次 buildx 无法给不同 platform 传不同 `BUILD_FROM`（需改 Dockerfile 按 `TARGETARCH` 选 base，与「Dockerfile 保持原样」冲突），且无消费者需要（Supervisor 用 `{arch}` tag），放弃。

**Consequences**：
- manifest 仍为 `source: local`：sync-addons.py / rewrite-images.py / check-images.py 继续跳过该 add-on，`image:` 不会被改写、不会被可达性硬校验（经 ghcr.nju.edu.cn pull-through 兜底，可接受，记录于此）。
- 版本升级流程变化：改 config.yaml `version:` 后需重跑构建工作流（push main 命中 `haos-mirror-switcher/**` 路径过滤器即自动触发，或 workflow_dispatch）推新 tag；Supervisor 拉 `<image>:<version>` 保持一致。
- 预构建镜像通过 `ghcr.nju.edu.cn` 国内入口可达；运行时由 `haos-mirror-switcher` 另行维护 `registries_mirror`，两者是不同层次。
- Dockerfile 保留 `ARG BUILD_FROM` + `FROM $BUILD_FROM`，作为构建工作流与未来本地回退的双重配方。
- addon-authoring 规范 / check-addon C9 / check-docker D08 豁免约定需同步更新 `.codex/` 镜像副本。
