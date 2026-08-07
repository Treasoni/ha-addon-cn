# Docker / Dockerfile 规范（通用最佳实践 + 本仓库 add-on 镜像约定）

---
paths:
  - "Dockerfile"
  - "build.json"
  - "build.yaml"
  - "config.yaml"
  - "docker-compose*.yml"
  - ".dockerignore"
  - ".claude/templates/docker/**"
  - ".claude/scripts/check-docker.sh"
---

本规则定义 agent 生成 Docker 镜像时应遵循的铁律：**通用 Dockerfile 最佳实践**（仓库里非 add-on 的镜像构建）与**本仓库 add-on 镜像约定**（`*/Dockerfile` + `build.json`/`build.yaml` + `config.yaml` 的 `image:`）。生成新镜像、Dockerfile、构建配置或 docker-compose 文件时先读本规则；事后用 `.claude/scripts/check-docker.sh` 校验。

## 术语（与 CONTEXT.md 一致，不重定义）

- **add-on 商店**：本仓库根目录即 HA Add-on 商店，每个 `{slug}/` 目录一个 add-on。
- **vendored add-on**：从上游（alexbelgium / frenck / official）同步并镜像的 add-on；`source` 非 local。
- **source: local**：自有 add-on（`sync-addons.py --new-addon` 脚手架产物）；同步脚本永不触碰。
- **镜像地址重写（image rewrite）**：把 `image:` 行的 registry 主机换成国内镜像源的脚本化幂等变换。
- **镜像源 / registry proxy**：pull-through 代理 ghcr.io 的国内镜像站（如 `ghcr.nju.edu.cn`）。

本规则只讲「怎么写 Dockerfile / 构建配置」；「怎么改 `image:` 主机 / 验证镜像源」全部以 [[mirror-sources]] 为准，本节只链接不重复。

## 通用 Dockerfile 铁律（非 add-on）

每条：铁律 → 反例 → 正例。

**(a) 基础镜像 pinning — 禁 latest / 浮动 tag**
- `FROM` 必须用具体版本 tag；禁止 `latest`、`stable`、`alpine` 这类浮动 tag，禁止裸仓库名（隐式 latest）。
- digest pin（`FROM image@sha256:...`）仅允许**非 add-on** 的生产镜像；**add-on 一律禁止 digest**（tag 必须可读，镜像源工具依赖 tag 探测）。
- 反例：`FROM node:latest` / `FROM ghcr.io/x/y:stable` / `FROM debian`
- 正例：`FROM node:22.14.0-bookworm-slim`（生产可用 digest pin）
- 例外：add-on 必须 `FROM $BUILD_FROM`（见「add-on 镜像约定」），不做普通 pin。

**(b) 多阶段构建 + 构建上下文精简**
- 需要编译/安装工具的镜像必须多阶段构建：builder 阶段装工具链，最终阶段只 `COPY --from=` 产物；工具链不进最终镜像。
- `.dockerignore` 必须排除 `.git/`、`node_modules/`、`.cache/`、测试/文档、`docker-compose*`、`Dockerfile*` 与密钥（参照 `.claude/templates/docker/.dockerignore`）。
- 正例：`FROM ... AS build` 里 `npm ci && npm run build`，`FROM ...` 里 `COPY --from=build /app/dist /app`。
- 反例：单阶段 `RUN npm install -g @vue/cli && npm run build` 不清理。

**(c) 非 root USER**
- 通用镜像必须 `USER` 非 root（数值 uid 优先：`useradd -r -u 10001 app` → `USER 10001`）；确需 root 必须显式豁免注释。
- 反例：省略 `USER`（隐式 root）。
- 豁免：add-on 镜像运行在 Supervisor 下、需挂载卷写 `/data`，允许 root，但能降权必须降（见「add-on 镜像约定」）。

**(d) HEALTHCHECK**
- 长驻服务必须有 `HEALTHCHECK`（HTTP 探针优先）；一次性任务/短生命周期可豁免并注释理由。
- 正例：`HEALTHCHECK CMD curl --fail http://127.0.0.1:8080/health || exit 1`
- 反例：长驻服务无 HEALTHCHECK。

**(e) 无密钥/敏感信息**
- `ENV`/`ARG`/`RUN` 不得出现明文密钥/token/密码；不得 `COPY .env`、`*.pem`、`*.key`、含密钥的配置文件。
- `docker history` 会暴露每一层——删除变量**不**消除已写入层的值，须同层清理或多阶段。
- 反例：`ENV MYSQL_PASSWORD=123456`；`ARG AWS_SECRET_ACCESS_KEY=xxx`；`RUN echo $TOKEN > /app/token`
- 正例：密钥走运行时注入（add-on 走 config.yaml `options` / Supervisor 注入），镜像层零敏感值。

**(f) 镜像精简**
- 合并 RUN（`&&` 链式 + `\` 换行）；`apk add --no-cache` / `apt-get install -y --no-install-recommends`；同层清理缓存（`rm -rf /var/lib/apt/lists/*`）。
- 反例：每包一条 RUN；`apk add curl && apk add jq`；不清 apt 缓存。
- 正例：`RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*`

**(g) org.opencontainers.* LABEL 与可复现构建**
- 发布镜像必须带 OCI 标签（至少 `org.opencontainers.image.source` 与 `org.opencontainers.image.revision`），值来自 `ARG BUILD_SOURCE`/`BUILD_REVISION`/`BUILD_VERSION`（构建系统 `--build-arg` 注入），保证可追溯、可复现。
- 反例：无任何标签的裸镜像；`ENV BUILD_DEPS="$(...)"` 这类不可复现的构建期值。

**(h) CMD/ENTRYPOINT exec 形式 + PID 1 信号处理**
- `CMD`/`ENTRYPOINT` 用 JSON 数组（exec 形式）；禁止 shell 形式字符串（`CMD npm start` → `/bin/sh -c`，PID 1 收不到 SIGTERM、产生僵尸进程）。
- 长驻服务用 `tini`/s6 托管或自身处理 SIGTERM/SIGINT 优雅退出；入口脚本里前台进程必须 `exec` 接管。
- 正例：`CMD ["node", "app.js"]`；`ENTRYPOINT ["tini", "--", "cmd"]`

## 本仓库 add-on 镜像约定

1. **build.json / build.yaml `build_from` per-arch**
   - add-on 基础镜像在 `build.json`（JSON）或 `build.yaml`（YAML）里按 arch 映射；`build_from` 的每个值必须是具体版本 tag，**禁止 `latest`**；`args:`（build.yaml）放构建参数。
   - `arch` 声明在 `config.yaml` 的 `arch:` 列表，**不在** build.json/build.yaml。
   - 反例：`"ghcr.io/autobrr/autobrr:latest"`（仓库现存反例，新 add-on 禁用）。
   - 正例：见 `.claude/templates/docker/build.json`。
2. **ARG BUILD_FROM + FROM $BUILD_FROM**
   - add-on Dockerfile 第一行必须是 `ARG BUILD_FROM`，随后 `FROM $BUILD_FROM`（或 `${BUILD_FROM}`）；禁止在 Dockerfile 里硬编码基础镜像。
   - 反例：`FROM ghcr.io/x/y:1.2.3`（绕过 build_from，构建不按 arch 走）。
   - 正例：见 `.claude/templates/docker/Dockerfile.addon`。
3. **config.yaml `image:` {arch} 形态**
   - `image:` 只允许四种形状，不发明第五种：`<registry>/<ns>/<slug>-{arch}`、`<registry>/<ns>/<slug>`（无占位符）、`<registry>/<ns>/<slug>/{arch}`、官方形态 `<ns>/{arch}-addon-<slug>`（官方为 `homeassistant/{arch}-addon-x`，hacs-china 等源同族，`check-docker.sh` D08 已覆盖）。
   - `image:` 的 registry 主机改写只由 `rewrite-images.py`/同步管道完成，**agent 不手工改**（见 [[mirror-sources]]）。
   - `config.yaml` 的 `version` 必须是合法 tag（`^[A-Za-z0-9_][A-Za-z0-9_.-]{0,127}$`）——Supervisor 拉的是 `<image>:<version>`。
4. **version pinning 用 config.yaml version**
   - add-on 的版本 pin 用 `config.yaml` 的 `version` 字段；发布 tag = version。
   - 探测/校验镜像源必须用 config.yaml 真实 version，**绝不用 `latest`/`tags/list`**（两个坑见 [[mirror-sources]]）。
5. **run.sh `#!/usr/bin/with-contenv bashio`**
   - 自有/脚手架 add-on 入口脚本以 `#!/usr/bin/with-contenv bashio` 开头（Supervisor 注入 bashio + 环境），`set -e`；读 options 用 `bashio::config`、写日志用 `bashio::log.*`；长驻进程必须 `exec` 接管。
   - 反例：`#!/bin/sh` + 非 exec 的 `sleep infinity`。
6. **io.hass.* + org.opencontainers.* labels**
   - add-on 发布镜像必须带 `io.hass.name/description/arch/type="addon"/version` 与 `org.opencontainers.image.*`（source/revision/created 等），值来自 `ARG BUILD_NAME/BUILD_ARCH/BUILD_VERSION/BUILD_REPOSITORY/BUILD_REF/BUILD_DATE`（构建系统注入）。
   - 正例：见 `autobrr/Dockerfile` 的 Labels 段（alexbelgium house style）。
7. **source: local 保护**
   - `source: local` 的自有 add-on 永不被同步脚本触碰；改动其 Dockerfile/run.sh 走脚手架 + 本地编辑；`image:` 永不被改写（见 [[mirror-sources]]）。
8. **不碰 build_from**
   - **不碰 `build.json`/`build.yaml` 的 `build_from`**——那是本地构建的 base image，商店安装拉发布镜像（config.yaml `image`），与镜像地址重写无关；镜像重写只动 config.yaml 的 `image:` 主机前缀，且不改写 24 个官方 add-on、不动 `source: local`。一切以 [[mirror-sources]] 为准。

## docker-compose / docker CLI 本地测试

本仓库当前无 compose 文件；新增规范如下（仅本地调试，add-on 发布/安装由 HA Supervisor 构建，不走 compose）。

- compose 结构：`services.<name>` 全小写连字符；用 Compose v2 语法（省略 `version:`）；容器名由 `<project>-<service>-1` 生成，别硬依赖。
- volumes：命名卷或 bind mount，禁止容器内写宿主绝对路径。
- `env_file: .env`——`.env` 已被 `.gitignore` 忽略，compose 里不写明文密钥；配合 [[env]]。
- `healthcheck:` 可在 compose 覆盖 Dockerfile 的 `HEALTHCHECK`，测试用。
- 本地测试命令：`docker compose config`（校验语法）、`docker build --progress=plain -t test .`、`docker run --rm -it --init -p 8080:8080 test`。
- `.dockerignore` 记得排除 `docker-compose*`。

## 校验门禁（check-docker.sh）

- 改完 Dockerfile / build.json / build.yaml / config.yaml / 模板后运行 `.claude/scripts/check-docker.sh`。
- 默认只查**本次改动**文件 + 模板一致性（不会因仓库存量 `latest` 误报）；`--all` 全量扫描会列出存量欠债（当前约 77 个 build.json 用 latest，属既有基线，非本次引入）。
- 豁免标记：`# hadolint ignore=DL30xx`（沿用仓库惯例）或 `# check-docker: exempt` 内联注释。

```bash
# 默认：本次改动文件 + add-on 模板一致性
.claude/scripts/check-docker.sh
# 指定文件或 add-on 目录（可重复）
.claude/scripts/check-docker.sh --path grafana --path custom/Dockerfile
# 仅 add-on 模板一致性
.claude/scripts/check-docker.sh --addon-consistency
# 全量扫描（含存量基线欠债）
.claude/scripts/check-docker.sh --all
```
