#!/usr/bin/with-contenv bashio

set -e

# __NAME__（__SLUG__）启动脚本
# 从这里开始写你的逻辑。示例：

bashio::log.info "正在启动 __NAME__ ..."

# 读取 config.yaml 里的 options 配置：
# MESSAGE=$(bashio::config 'message')
# bashio::log.info "message: ${MESSAGE}"

# 长驻进程示例（你自己的服务替换这行）：
# exec your-service --foreground
sleep infinity
