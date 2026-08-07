ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# python3: 内嵌 ingress Web 界面（stdlib，无第三方依赖）
# docker-cli: 经挂载的 docker socket 操作 hassio_supervisor 容器（docker exec / docker cp）
# dbus: 经 host_dbus 挂载的宿主 /run/dbus 调 RAUC Installer.Install（OTA 安装）
RUN apk add --no-cache python3 docker-cli dbus

COPY run.sh /run.sh
COPY server.py /server.py
COPY lib /lib
COPY www /www
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
