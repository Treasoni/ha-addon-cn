ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# unzip: 解压 gitee 源码 zip 与前端轮子（wheel 即 zip）
# curl: 下载 gitee / tuna 制品（显式安装，不依赖 base 是否自带）
RUN apk add --no-cache unzip curl

COPY run.sh /run.sh
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
