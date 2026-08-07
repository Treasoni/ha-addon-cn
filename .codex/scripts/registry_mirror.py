#!/usr/bin/env python3
"""
HA Add-on 商店「镜像地址重写」共享模块。

把 add-on config.yaml 里 `image:` 的 `ghcr.io` 主机前缀改写为国内 registry 代理（镜像源），
并提供镜像源探测与逐镜像校验。无第三方依赖（urllib）。

验证方法学与已知清单见 .codex/rules/common/mirror-sources.md：
  - 探测必须打 manifest 端点 + config.yaml 的真实 version；
  - 不要用 /v2/<repo>/tags/list（pull-through 代理对未缓存仓库返回假 NAME_UNKNOWN）；
  - 不要用 latest tag（frenck / 官方镜像没有 latest）。
"""
from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # Windows 控制台避免中文乱码

# 候选镜像源（pull-through 代理 ghcr.io）。顺序即优先顺序，第一个为默认。
# 新增候选：先用 probe_image() 验证，再把 host 追加到列表并同步到规则文件。
KNOWN_MIRRORS = [
    "ghcr.nju.edu.cn",  # 南京大学镜像站；2026-08-07 实测 alexbelgium / frenck 均 200
]

GHCR_HOST = "ghcr.io"

_MANIFEST_ACCEPT = ", ".join(
    [
        "application/vnd.docker.distribution.manifest.list.v2+json",
        "application/vnd.oci.image.index.v1+json",
        "application/vnd.docker.distribution.manifest.v2+json",
        "application/vnd.docker.distribution.manifest.v1+json",
        "application/json",
    ]
)

_USER_AGENT = "ha-addon-registry-check/1.0"


# --------------------------------------------------------------------------- #
# YAML 字段 / 文本改写
# --------------------------------------------------------------------------- #
def yaml_field(text: str, field: str) -> str | None:
    """从 config.yaml 文本里读一个顶层标量字段（无第三方 YAML 依赖）。"""
    m = re.search(rf"^{field}:\s*[\"']?([^\"'\s#]+)", text, re.MULTILINE)
    return m.group(1) if m else None


def image_host(image: str) -> str:
    """取镜像引用里的 registry 主机；Docker Hub 简写（namespace/name）返回 namespace。"""
    if "://" in image:
        image = image.split("://", 1)[1]
    return image.split("/", 1)[0] if "/" in image else ""


def _mirror_hosts() -> set[str]:
    return {GHCR_HOST} | set(KNOWN_MIRRORS)


def transform_yaml(text: str, mirror: str) -> str:
    """幂等改写：把 `image:` 行的 registry 主机换成镜像源。

    仅当主机是 ghcr.io 或任一已知镜像源时才替换（支持换源迁移）；已是目标
    镜像源则不变，天然幂等。保留原行缩进、引号与 `{arch}` 占位符形状
    （`-{arch}` 与 `/{arch}` 两种），其余内容原样不动。
    """
    mirror = mirror.rstrip("/")
    hosts = "|".join(re.escape(h) for h in _mirror_hosts())
    pat = re.compile(rf"(?m)^(\s*image\s*:\s*[\"']?)(?:{hosts})/")

    def _repl(m: re.Match) -> str:
        return f"{m.group(1)}{mirror}/"

    return pat.sub(_repl, text)


def image_fields(config_path: Path) -> tuple[str | None, str | None]:
    """返回 config.yaml 的 (image, version)；读不了则 (None, None)。"""
    try:
        text = config_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None, None
    return yaml_field(text, "image"), yaml_field(text, "version")


def image_repo(image: str, arch: str = "amd64") -> str:
    """image 去掉 registry 主机与 {arch} 占位符，得到 registry 的 repo 路径。

    - `ghcr.io/alexbelgium/autobrr-{arch}` -> `alexbelgium/autobrr-amd64`
    - `homeassistant/{arch}-addon-git_pull`（Docker Hub 简写）-> `homeassistant/amd64-addon-git_pull`
    - `docker.io/foo/bar` -> `foo/bar`
    """
    repo = image
    if "://" in repo:
        repo = repo.split("/", 1)[1]
    elif "/" in repo and "." in repo.split("/", 1)[0]:
        # 首段是含点的 registry 主机（ghcr.io / docker.io / quay.io），去掉
        repo = repo.split("/", 1)[1]
    return repo.replace("{arch}", arch)


# --------------------------------------------------------------------------- #
# Registry 探测
# --------------------------------------------------------------------------- #
def http_status(url: str, timeout: float = 25.0) -> int:
    """GET 返回状态码；网络/超时错误返回 0（不抛异常）。"""
    req = urllib.request.Request(
        url, headers={"Accept": _MANIFEST_ACCEPT, "User-Agent": _USER_AGENT}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


def manifest_url(mirror: str, repo: str, version: str) -> str:
    return f"https://{mirror}/v2/{repo.lstrip('/')}/manifests/{version}"


def probe_image(mirror: str, repo: str, version: str, timeout: float = 25.0) -> int:
    """探测镜像在镜像源上是否可拉。2xx=可用；404=缺失；0=网络失败。"""
    return http_status(manifest_url(mirror, repo, version), timeout=timeout)


def pick_mirror(probes: list[tuple[str, str]], timeout: float = 25.0) -> str | None:
    """按 KNOWN_MIRRORS 顺序探测，返回第一个能拉到任一 probe 的镜像源。

    probes: [(repo, version), ...]；任一 probe 返回 2xx 即认为该源可用。
    全部失败返回 None。
    """
    for mirror in KNOWN_MIRRORS:
        for repo, ver in probes:
            code = probe_image(mirror, repo, ver, timeout=timeout)
            if 200 <= code < 300:
                print(f"[mirror] 选定镜像源 {mirror}（{repo}:{ver} -> {code}）")
                return mirror
            print(f"[mirror] {mirror} 探测 {repo}:{ver} -> {code}")
    return None


# --------------------------------------------------------------------------- #
# 逐镜像校验
# --------------------------------------------------------------------------- #
def check_ghcr(config_path: Path, mirror: str) -> tuple[str, bool, str]:
    """校验 ghcr 类 add-on（原始 ghcr.io 或已改写的镜像源前缀）：经镜像源以真实 version 探测。

    返回 (image, ok, detail)；ok=False 表示该 add-on 经当前镜像源不可拉。
    """
    img, ver = image_fields(config_path)
    if not img or image_host(img) not in _mirror_hosts():
        return (img or ""), True, "非 ghcr 镜像，跳过"
    repo = image_repo(img)
    if not ver:
        return img, False, "缺少 version 字段"
    code = probe_image(mirror, repo, ver)
    if 200 <= code < 300:
        return img, True, f"{repo}:{ver} -> {code}"
    return img, False, f"{repo}:{ver} -> {code}"


def check_docker_hub(config_path: Path) -> tuple[str, bool, str]:
    """校验 Docker Hub 类 add-on（如 homeassistant/{arch}-addon-x）存在性。信息级。

    返回 (image, ok, detail)。可达性因 HA 主机而异，ok=False 只作提示不阻断。
    """
    img, _ = image_fields(config_path)
    if not img or classify(img) != "dockerhub":
        return (img or ""), True, "跳过"
    name = image_repo(img)
    code = http_status(
        f"https://hub.docker.com/v2/repositories/{name}/tags", timeout=15.0
    )
    if code == 200:
        return img, True, f"hub.docker.com/{name}/tags -> 200"
    return img, False, f"hub.docker.com/{name}/tags -> {code}"


def classify(image: str) -> str:
    """镜像引用分类：'ghcr'（ghcr.io 或已知镜像源）| 'dockerhub'（Docker Hub 简写/显式）| 'other'。"""
    if not image:
        return "other"
    host = image_host(image)
    if host in _mirror_hosts():
        return "ghcr"
    if host in ("docker.io", "registry.hub.docker.com"):
        return "dockerhub"
    if host and "." not in host:
        return "dockerhub"  # Docker Hub 简写：namespace 无点
    return "other"
