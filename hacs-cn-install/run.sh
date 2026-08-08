#!/usr/bin/with-contenv bashio
# shellcheck shell=bash
set -Eeuo pipefail

# 固定版本：安装器本身不追踪分支、tag 或 GitHub Release。
HACS_TAG="2.0.5.3"
HACS_COMMIT="d1c828dd078736ec663951844786cf8285e18b4d"
FRONTEND_VERSION="20250128065759"
AIOGITHUBAPI_VERSION="24.6.0"

HACS_SOURCE_REF="$HACS_COMMIT"
HACS_SOURCE_URL="https://gitee.com/hacs-china/integration/repository/archive/${HACS_SOURCE_REF}.zip"
FRONTEND_URL="https://pypi.tuna.tsinghua.edu.cn/packages/6c/42/af2a204b462124f617727fd462fab243dd2aa01e1e202461daf810cda012/hacs_frontend-${FRONTEND_VERSION}-py3-none-any.whl"
AIOGITHUBAPI_URL="https://pypi.tuna.tsinghua.edu.cn/packages/c5/68/7f6b735c49f8257069a5bf50b4047f1bcd47341b485225fd58af788b7f53/aiogithubapi-${AIOGITHUBAPI_VERSION}-py3-none-any.whl"
FRONTEND_SHA256="e6b196171fbcb3cb3eced2c48e789f3dc946b59f7490487df16d8d4e47a85fc4"
AIOGITHUBAPI_SHA256="1bcbab282d70ba1c82deddc1d8e62825785d125aa8199328729d12a0a4a60da8"

WORK="$(mktemp -d /tmp/hacs-cn-install.XXXXXX)"
TARGET="/homeassistant/custom_components/hacs"
DEPS_DIR="/homeassistant/deps"
BACKUP_ROOT="/homeassistant/hacs-cn-backups"
REPLACE_EXISTING="$(bashio::config 'replace_existing' 'false')"
DEPS_MUTATED=0
TARGET_MOVED=0
TARGET_INSTALLED=0
INSTALL_COMMITTED=0
TARGET_BACKUP=""

log_step() {
  bashio::log.info "$1"
}

fail() {
  local code="$1"
  local message="$2"
  bashio::log.error "[${code}] ${message}"
  bashio::exit.nok "[${code}] ${message}"
  exit 1
}

rollback_deps() {
  [ "$DEPS_MUTATED" -eq 1 ] || return 0
  rm -rf "${DEPS_DIR}/aiogithubapi" "${DEPS_DIR}"/aiogithubapi-*.dist-info \
    "${DEPS_DIR}/.aiogithubapi-install" "${DEPS_DIR}"/.aiogithubapi-*.dist-info.install 2>/dev/null || true
  if [ -d "${WORK}/deps-backup" ]; then
    mkdir -p "$DEPS_DIR"
    cp -a "${WORK}/deps-backup/." "$DEPS_DIR/" 2>/dev/null || true
  fi
  DEPS_MUTATED=0
}

rollback_target() {
  [ "$INSTALL_COMMITTED" -eq 0 ] || return 0
  if [ "$TARGET_INSTALLED" -eq 1 ]; then
    rm -rf "$TARGET" 2>/dev/null || true
  fi
  if [ "$TARGET_MOVED" -eq 1 ] && [ -n "$TARGET_BACKUP" ] && [ -d "$TARGET_BACKUP" ]; then
    mv "$TARGET_BACKUP" "$TARGET" 2>/dev/null || true
  fi
}

cleanup() {
  rollback_target
  rollback_deps
  rm -rf "$WORK"
}
trap cleanup EXIT

download_verified() {
  local url="$1"
  local output="$2"
  local expected_sha="$3"
  local label="$4"
  curl -fL --retry 3 --retry-delay 2 --connect-timeout 20 --max-time 900 \
    -o "$output" "$url" \
    || fail "${label}_DOWNLOAD_FAILED" "${label} 下载失败，请确认 Gitee/TUNA 可达后重试"
  [ -s "$output" ] || fail "${label}_EMPTY" "${label} 下载结果为空"
  local actual_sha
  actual_sha="$(sha256sum "$output" | awk '{print $1}')"
  [ "$actual_sha" = "$expected_sha" ] \
    || fail "${label}_HASH_MISMATCH" "${label} 校验失败，已停止安装"
}

verify_hacs_stage() {
  local component="$1"
  [ -f "$component/manifest.json" ] \
    || fail "INSTALL_VERIFY_FAILED" "HACS manifest 缺失"
  python3 - "$component/manifest.json" "$HACS_TAG" "$HACS_COMMIT" <<'PY' \
    || fail "INSTALL_VERIFY_FAILED" "HACS manifest 校验失败"
import json
import sys

manifest_path, expected_version, expected_commit = sys.argv[1:]
with open(manifest_path, encoding="utf-8") as file:
    manifest = json.load(file)
if manifest.get("domain") != "hacs" or not manifest.get("name"):
    raise SystemExit("manifest domain is not hacs")
manifest["version"] = expected_version
with open(manifest_path, "w", encoding="utf-8") as file:
    json.dump(manifest, file, ensure_ascii=False, indent=2)
    file.write("\n")
print(f"validated HACS tag={expected_version} commit={expected_commit}")
PY
  [ -f "$component/hacs_frontend/version.py" ] \
    || fail "FRONTEND_VERIFY_FAILED" "前端文件缺失，无法完成安装"
  grep -q "$FRONTEND_VERSION" "$component/hacs_frontend/version.py" \
    || fail "FRONTEND_VERIFY_FAILED" "前端版本与固定版本不一致"
}

prepare_dependency() {
  local wheel="$1"
  mkdir -p "$WORK/deps-stage"
  unzip -q "$wheel" -d "$WORK/deps-stage" \
    || fail "DEPENDENCY_EXTRACT_FAILED" "aiogithubapi wheel 解压失败"
  PYTHONPATH="$WORK/deps-stage" python3 - "$AIOGITHUBAPI_VERSION" <<'PY' \
    || fail "DEPENDENCY_VERIFY_FAILED" "aiogithubapi 无法导入或版本不匹配"
import importlib.metadata
import sys
import aiogithubapi

expected = sys.argv[1]
actual = importlib.metadata.version("aiogithubapi")
if actual != expected:
    raise SystemExit(f"expected {expected}, got {actual}")
print(f"validated aiogithubapi={actual}")
PY
}

verify_installed() {
  [ -f "$TARGET/manifest.json" ] \
    || fail "INSTALL_VERIFY_FAILED" "安装后的 HACS manifest 缺失"
  python3 - "$TARGET/manifest.json" "$HACS_TAG" <<'PY' \
    || fail "INSTALL_VERIFY_FAILED" "安装后的 HACS manifest 校验失败"
import json
import sys
path, expected_version = sys.argv[1:]
with open(path, encoding="utf-8") as file:
    manifest = json.load(file)
if manifest.get("domain") != "hacs" or manifest.get("version") != expected_version:
    raise SystemExit("unexpected HACS manifest")
PY
  [ -f "$TARGET/hacs_frontend/version.py" ] \
    || fail "INSTALL_VERIFY_FAILED" "安装后的 HACS 前端文件缺失"
  grep -Fq "$FRONTEND_VERSION" "$TARGET/hacs_frontend/version.py" \
    || fail "INSTALL_VERIFY_FAILED" "安装后的 HACS 前端版本不匹配"
  PYTHONPATH="$DEPS_DIR" python3 - "$AIOGITHUBAPI_VERSION" <<'PY' \
    || fail "INSTALL_VERIFY_FAILED" "安装后的 aiogithubapi 无法导入"
import importlib.metadata
import sys
import aiogithubapi
expected = sys.argv[1]
if importlib.metadata.version("aiogithubapi") != expected:
    raise SystemExit("unexpected aiogithubapi version")
PY
}

install_dependency() {
  mkdir -p "$DEPS_DIR" "$WORK/deps-backup"
  local dist
  dist="$(find "$WORK/deps-stage" -maxdepth 1 -type d -name 'aiogithubapi-*.dist-info' | head -n 1)"
  [ -n "$dist" ] || fail "DEPENDENCY_PRELOAD_FAILED" "aiogithubapi metadata 缺失"
  rm -rf "$WORK/deps-atomic"
  mkdir -p "$WORK/deps-atomic"
  cp -a "$WORK/deps-stage/aiogithubapi" "$WORK/deps-atomic/" \
    || fail "DEPENDENCY_PRELOAD_FAILED" "无法准备 aiogithubapi 原子暂存目录"
  cp -a "$dist" "$WORK/deps-atomic/" \
    || fail "DEPENDENCY_PRELOAD_FAILED" "无法准备 aiogithubapi metadata 暂存目录"
  PYTHONPATH="$WORK/deps-atomic" python3 - "$AIOGITHUBAPI_VERSION" <<'PY' \
    || fail "DEPENDENCY_PRELOAD_FAILED" "暂存依赖无法导入或版本不匹配"
import importlib.metadata
import sys
import aiogithubapi
if importlib.metadata.version("aiogithubapi") != sys.argv[1]:
    raise SystemExit("unexpected staged aiogithubapi version")
PY
  shopt -s nullglob
  local old
  for old in "$DEPS_DIR/aiogithubapi" "$DEPS_DIR"/aiogithubapi-*.dist-info; do
    [ -e "$old" ] || continue
    mv "$old" "$WORK/deps-backup/"
  done
  shopt -u nullglob
  DEPS_MUTATED=1
  rm -rf "$DEPS_DIR/.aiogithubapi-install" "$DEPS_DIR"/.aiogithubapi-*.dist-info.install
  mv "$WORK/deps-atomic/aiogithubapi" "$DEPS_DIR/.aiogithubapi-install" \
    || fail "DEPENDENCY_PRELOAD_FAILED" "无法写入 Home Assistant deps 暂存目录"
  mv "$DEPS_DIR/.aiogithubapi-install" "$DEPS_DIR/aiogithubapi" \
    || fail "DEPENDENCY_PRELOAD_FAILED" "无法原子替换 aiogithubapi"
  local staged_dist
  staged_dist="$(find "$WORK/deps-atomic" -maxdepth 1 -type d -name 'aiogithubapi-*.dist-info' | head -n 1)"
  mv "$staged_dist" "$DEPS_DIR/.$(basename "$staged_dist").install" \
    || fail "DEPENDENCY_PRELOAD_FAILED" "无法写入 aiogithubapi metadata 暂存目录"
  mv "$DEPS_DIR"/.aiogithubapi-*.dist-info.install "$DEPS_DIR/" \
    || fail "DEPENDENCY_PRELOAD_FAILED" "无法原子替换 aiogithubapi metadata"
}

log_step "HACS 国内安装器启动：固定版本 ${HACS_TAG}，来源 Gitee + 清华 TUNA"

if [ -e "$TARGET" ] && [ "$REPLACE_EXISTING" != "true" ]; then
  fail "EXISTING_HACS_REQUIRES_CONFIRMATION" \
    "检测到已有 HACS。请在配置中将 replace_existing 改为 true 后再启动；当前未修改任何文件"
fi

mkdir -p "$WORK/src" "$WORK/component-stage"

log_step "① 下载并解压 Gitee HACS China tag=${HACS_TAG}（commit=${HACS_COMMIT}）"
curl -fL --retry 3 --retry-delay 2 --connect-timeout 20 --max-time 900 \
  -o "$WORK/hacs-src.zip" "$HACS_SOURCE_URL" \
  || fail "SOURCE_UNREACHABLE" "Gitee 源码下载失败，请确认 gitee.com 可达后重试"
[ "$(wc -c < "$WORK/hacs-src.zip")" -gt 100000 ] \
  || fail "SOURCE_INVALID" "Gitee 源码压缩包体积异常"
unzip -q "$WORK/hacs-src.zip" -d "$WORK/src" \
  || fail "SOURCE_EXTRACT_FAILED" "Gitee 源码解压失败"
SRC="$(find "$WORK/src" -type d -path '*/custom_components/hacs' | head -n 1)"
[ -n "$SRC" ] || fail "SOURCE_INVALID" "源码中未找到 custom_components/hacs"
cp -a "$SRC/." "$WORK/component-stage/"

log_step "② 下载并校验前端 wheel=${FRONTEND_VERSION}"
download_verified "$FRONTEND_URL" "$WORK/frontend.whl" "$FRONTEND_SHA256" "FRONTEND"
unzip -q -o "$WORK/frontend.whl" -d "$WORK/component-stage" \
  || fail "FRONTEND_EXTRACT_FAILED" "前端 wheel 解压失败"
rm -rf "$WORK/component-stage"/*.dist-info

log_step "③ 固定 HACS manifest 版本并验证安装内容"
verify_hacs_stage "$WORK/component-stage"

log_step "④ 下载、校验并预置 aiogithubapi=${AIOGITHUBAPI_VERSION} 到 /config/deps"
download_verified "$AIOGITHUBAPI_URL" "$WORK/aiogithubapi.whl" "$AIOGITHUBAPI_SHA256" "DEPENDENCY"
prepare_dependency "$WORK/aiogithubapi.whl"
install_dependency

log_step "⑤ 原子备份并安装 custom_components/hacs"
mkdir -p "$(dirname "$TARGET")" "$BACKUP_ROOT"
if [ -e "$TARGET" ]; then
  TARGET_BACKUP="$BACKUP_ROOT/hacs-$(date +%Y%m%d%H%M%S)-$$"
  mv "$TARGET" "$TARGET_BACKUP" \
    || fail "BACKUP_FAILED" "已有 HACS 备份失败，未覆盖原目录"
  TARGET_MOVED=1
  bashio::log.info "已有 HACS 已备份到 ${TARGET_BACKUP}"
fi
mv "$WORK/component-stage" "$TARGET" \
  || fail "INSTALL_FAILED" "无法写入 ${TARGET}"
TARGET_INSTALLED=1
verify_installed
INSTALL_COMMITTED=1
DEPS_MUTATED=0

shopt -s nullglob
backups=("$BACKUP_ROOT"/hacs-*)
if [ "${#backups[@]}" -gt 3 ]; then
  IFS=$'\n' backups=( $(ls -1dt "${backups[@]}" 2>/dev/null) )
  for ((i=3; i<${#backups[@]}; i++)); do
    rm -rf "${backups[$i]}"
  done
fi
shopt -u nullglob

bashio::log.info "安装完成：HACS ${HACS_TAG} + 前端 ${FRONTEND_VERSION}"
bashio::log.info "下一步：重启 Home Assistant，然后到 设置 → 设备与服务 → 添加集成 → 搜索 HACS"
bashio::log.info "说明：这是 HACS China 第三方 fork；HACS 安装后的仓库访问仍依赖 fork 自带代理，公益代理无 SLA"
bashio::exit.ok
