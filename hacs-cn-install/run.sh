#!/usr/bin/with-contenv bashio
# shellcheck shell=bash
set -e

INTEGRATION_VERSION="$(bashio::config 'integration_version' '2.0.5.3')"
FE_VERSION="20250128065759"
WORK="/tmp/hacs-cn-install"
TARGET="/homeassistant/custom_components/hacs"

bashio::log.info "========================================="
bashio::log.info "HACS 极速版 Gitee 安装器（hacs-cn-install）"
bashio::log.info "integration_version=${INTEGRATION_VERSION}  frontend=${FE_VERSION}"
bashio::log.info "========================================="

rm -rf "${WORK}"
mkdir -p "${WORK}"

# ---------- 1) 下载 gitee 源码（china 分支） ----------
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

# ---------- 2) 下载并解压前端轮子（清华 tuna 镜像） ----------
bashio::log.info "② 从 tuna 镜像解析并下载 hacs_frontend==${FE_VERSION} 轮子..."
WHEEL_REL="$(curl -fsSL --connect-timeout 20 "https://pypi.tuna.tsinghua.edu.cn/simple/hacs_frontend/" \
  | grep -oE "href=\"[^\"]*${FE_VERSION}[^\"]*\.whl[^\"]*\"" | head -n1 \
  | sed 's/^href="//; s/"$//')"
[ -n "${WHEEL_REL}" ] || bashio::exit.nok "tuna 上未找到 hacs_frontend==${FE_VERSION} 轮子"
WHEEL_URL="https://pypi.tuna.tsinghua.edu.cn/${WHEEL_REL#../../}"
curl -fL --retry 3 --connect-timeout 20 -o "${WORK}/frontend.whl" "${WHEEL_URL}" \
  || bashio::exit.nok "下载前端轮子失败（请检查 tuna 连通性）"
[ "$(wc -c < "${WORK}/frontend.whl")" -gt 1000000 ] \
  || bashio::exit.nok "前端轮子异常（体积过小）"
unzip -q -o "${WORK}/frontend.whl" -d "${SRC}"
rm -rf "${SRC}"/*.dist-info
bashio::log.info "前端已解压进 custom_components/hacs（hacs_frontend/）"

# ---------- 3) 注入版本号（china 分支 manifest 为 0.0.0） ----------
sed -i "s/\"version\": \"0.0.0\"/\"version\": \"${INTEGRATION_VERSION}\"/" "${SRC}/manifest.json"
bashio::log.info "③ manifest version -> ${INTEGRATION_VERSION}"

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
