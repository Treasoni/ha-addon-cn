#!/usr/bin/with-contenv bashio
# shellcheck shell=bash
set -euo pipefail

# ---------- 1) 读取 options ----------
AUTO_SWITCH="$(bashio::config 'auto_switch')"
PROBE_INTERVAL_HOURS="$(bashio::config 'probe_interval_hours')"
PROBE_TIMEOUT="$(bashio::config 'probe_timeout_seconds')"
ENABLE_GHCR="$(bashio::config 'enable_ghcr')"
ENABLE_DOCKERIO="$(bashio::config 'enable_dockerio')"
ENABLE_LSCR="$(bashio::config 'enable_lscr')"
ENABLE_OTA="$(bashio::config 'enable_ota')"
INGRESS_PORT="$(bashio::addon.ingress_port 2>/dev/null || echo 8569)"
export INGRESS_PORT

export PROBE_TIMEOUT ENABLE_GHCR ENABLE_DOCKERIO ENABLE_LSCR ENABLE_OTA
export AUTO_SWITCH PROBE_INTERVAL_HOURS
export SLUG="haos-mirror-switcher"

# ---------- 2) Docker socket 检测（portainer 先例：/var/run 优先，/run 回退） ----------
SOCK=""
[ -S /var/run/docker.sock ] && SOCK=/var/run/docker.sock
[ -z "$SOCK" ] && [ -S /run/docker.sock ] && SOCK=/run/docker.sock
if [ -n "$SOCK" ]; then
  bashio::log.info "使用 docker socket：${SOCK}"
  export DOCKER_HOST="unix://${SOCK}"
else
  bashio::log.warning "未检测到 docker socket —— 请在加载项页面关闭“保护模式”后重新启动；当前 Web 界面只能查看状态，无法写 docker.json / OTA"
fi

# ---------- 3) 共享动作模块 + 启动自愈 ----------
source /lib/actions.sh
bashio::log.info "启动自愈检查…"
self_heal || bashio::log.warning "启动自愈未完成，请打开 Web 界面处理"

# ---------- 4) 启动 Web 界面（后台） ----------
bashio::log.info "启动 Web 界面（ingress 端口 ${INGRESS_PORT}）"
python3 /server.py &
SERVER_PID=$!

trap 'bashio::log.info "收到退出信号，退出"; kill "$SERVER_PID" 2>/dev/null || true; exit 0' TERM INT

# ---------- 5) 前台周期探测主循环 ----------
bashio::log.info "已启动：自动换源=${AUTO_SWITCH}，探测间隔=${PROBE_INTERVAL_HOURS}h，OTA=${ENABLE_OTA}"
INTERVAL_SECONDS=$(( PROBE_INTERVAL_HOURS * 3600 ))
while true; do
  sleep "$INTERVAL_SECONDS"
  if [ "$AUTO_SWITCH" = "true" ]; then
    bashio::log.info "周期探测镜像源…"
    auto_switch_cycle || bashio::log.warning "本次探测周期出现异常（已记录，继续等待下一周期）"
  fi
done
