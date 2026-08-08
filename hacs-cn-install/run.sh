#!/usr/bin/with-contenv bashio
# shellcheck shell=bash
set -e

INTEGRATION_VERSION="$(bashio::config 'integration_version' '2.0.5.3')"
WORK="/tmp/hacs-cn-install"
TARGET="/homeassistant/custom_components/hacs"

bashio::log.info "========================================="
bashio::log.info "HACS 极速版 Gitee 安装器（hacs-cn-install）"
bashio::log.info "integration_version 默认 = ${INTEGRATION_VERSION}（运行时优先取 gitee 最新 tag）"
bashio::log.info "========================================="

rm -rf "${WORK}"
mkdir -p "${WORK}"

# ---------- 1) 下载 gitee 源码（china 分支，实时快照） ----------
bashio::log.info "① 下载 gitee 源码（china 分支）..."
curl -fL --retry 3 --connect-timeout 20 \
  -o "${WORK}/hacs-src.zip" \
  "https://gitee.com/hacs-china/integration/repository/archive/china.zip" \
  || bashio::exit.nok "下载 gitee 源码失败（请检查 gitee.com 连通性）"
[ "$(wc -c < "${WORK}/hacs-src.zip")" -gt 100000 ] \
  || bashio::exit.nok "gitee 源码 zip 异常（体积过小）"
unzip -q "${WORK}/hacs-src.zip" -d "${WORK}/src"
SRC="$(find "${WORK}/src" -type d -path '*/custom_components/hacs' | head -n1)"
[ -n "${SRC}" ] || bashio::exit.nok "gitee 源码中未找到 custom_components/hacs"

# ---------- 2) 前端轮子：版本与集成源码自动对齐 ----------
# 从源码 scripts/install/frontend 解析 FRONTEND_VERSION（上游 pin，不硬编码）
FE_SCRIPT="$(find "${WORK}/src" -path '*/scripts/install/frontend' -type f | head -n1)"
[ -n "${FE_SCRIPT}" ] || bashio::exit.nok "源码中未找到 scripts/install/frontend（无法确定前端版本）"
FE_VERSION="$(sed -n 's/.*FRONTEND_VERSION="\([^"]*\)".*/\1/p' "${FE_SCRIPT}" | head -n1)"
[ -n "${FE_VERSION}" ] || bashio::exit.nok "无法从 install/frontend 解析 FRONTEND_VERSION"
bashio::log.info "② 前端版本（对齐集成源码）：${FE_VERSION}"
bashio::log.info "   从 tuna 镜像解析并下载 hacs_frontend==${FE_VERSION} 轮子..."
WHEEL_REL="$(curl -fsSL --connect-timeout 20 "https://pypi.tuna.tsinghua.edu.cn/simple/hacs_frontend/" \
  | grep -oE "href=\"[^\"]*${FE_VERSION}[^\"]*\.whl[^\"]*\"" | head -n1 \
  | sed 's/^href="//; s/"$//')"
[ -n "${WHEEL_REL}" ] || bashio::exit.nok "tuna 上未找到 hacs_frontend==${FE_VERSION} 轮子（上游 pin 可能已更新，重试或等 add-on 更新）"
WHEEL_URL="https://pypi.tuna.tsinghua.edu.cn/${WHEEL_REL#../../}"
curl -fL --retry 3 --connect-timeout 20 -o "${WORK}/frontend.whl" "${WHEEL_URL}" \
  || bashio::exit.nok "下载前端轮子失败（请检查 tuna 连通性）"
[ "$(wc -c < "${WORK}/frontend.whl")" -gt 1000000 ] \
  || bashio::exit.nok "前端轮子异常（体积过小）"
unzip -q -o "${WORK}/frontend.whl" -d "${SRC}"
rm -rf "${SRC}"/*.dist-info
bashio::log.info "前端已解压进 custom_components/hacs（hacs_frontend/）"

# ---------- 3) 注入版本号：优先取 gitee 最新 china tag，失败回退 options 默认 ----------
bashio::log.info "③ 查询 gitee 最新 china tag..."
ALL_TAGS=""
for page in 1 2 3; do
  ALL_TAGS="${ALL_TAGS}$(curl -fsSL --connect-timeout 15 "https://gitee.com/api/v5/repos/hacs-china/integration/tags?per_page=100&page=${page}" 2>/dev/null || true)\n"
done
LATEST_TAG="$(printf '%b' "${ALL_TAGS}" \
  | grep -oE '"name": ?"[0-9]+(\.[0-9]+)+"' \
  | sed -E 's/.*"([0-9]+(\.[0-9]+)+)".*/\1/' \
  | sort -t. -k1,1n -k2,2n -k3,3n -k4,4n \
  | tail -n1)"
if [ -n "${LATEST_TAG}" ]; then
  INTEGRATION_VERSION="${LATEST_TAG}"
  bashio::log.info "注入版本（gitee 最新 china tag）：${INTEGRATION_VERSION}"
else
  bashio::log.warning "gitee tag 查询失败，回退 options 默认版本：${INTEGRATION_VERSION}"
fi
sed -i "s/\"version\": \"0.0.0\"/\"version\": \"${INTEGRATION_VERSION}\"/" "${SRC}/manifest.json"

# ---------- 4) 兜底：预下载 aiogithubapi 轮子（pypi.org 被墙时手动安装用） ----------
bashio::log.info "④ 预下载 aiogithubapi 轮子到 /homeassistant/hacs-gitee-deps/ ..."
DEPS="/homeassistant/hacs-gitee-deps"
mkdir -p "${DEPS}"
W2="$(curl -fsSL --connect-timeout 20 "https://pypi.tuna.tsinghua.edu.cn/simple/aiogithubapi/" \
  | grep -oE 'href="[^"]*aiogithubapi-[0-9][^"]*-py3-none-any\.whl[^"]*"' | tail -n1 \
  | sed 's/^href="//; s/"$//')"
if [ -n "${W2}" ]; then
  FN="${W2##*/}"
  FN="${FN%%#*}"
  curl -fL --retry 3 --connect-timeout 20 -o "${DEPS}/${FN}" \
    "https://pypi.tuna.tsinghua.edu.cn/${W2#../../}" \
    || bashio::log.warning "预下载 aiogithubapi 失败（不阻塞安装，稍后手动处理）"
else
  bashio::log.warning "tuna 未找到 aiogithubapi 轮子（不阻塞安装）"
fi

# ---------- 5) 备份并拷贝到 HA 配置目录 ----------
if [ -d "${TARGET}" ]; then
  mv "${TARGET}" "${TARGET}.bak-$(date +%Y%m%d%H%M%S)"
  bashio::log.info "已备份原 HACS 到 ${TARGET}.bak-*"
fi
mkdir -p /homeassistant/custom_components
cp -a "${SRC}" "${TARGET}"

bashio::log.info "========================================="
bashio::log.info "安装完成！下一步：重启 Home Assistant → 设置→设备与服务 → 添加集成 → 搜索 HACS"
bashio::log.info "若 pypi.org 不可达导致 HACS 加载失败，用 /homeassistant/hacs-gitee-deps/ 下的轮子手动安装 aiogithubapi（见 README 常见问题）"
bashio::log.info "========================================="
bashio::exit.ok
