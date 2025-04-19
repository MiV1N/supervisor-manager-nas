FROM python:3.9-slim-buster

# 安装 Supervisor 和 Web UI 相关依赖
# 创建 Supervisor 配置文件目录和    日志目录  理服务的脚本存放路径
RUN pip install --no-cache-dir supervisor Flask && \
mkdir -p /etc/supervisor/conf.d  /var/log/supervisor app/manage_services

# 将 Supervisor 配置文件复制到容器中 (可以被挂载覆盖)
COPY supervisord.conf /etc/supervisor/supervisord.conf

# 创建管理服务的脚本
COPY manage_services.py /app/manage_services/manage_services.py

# 设置工作目录
WORKDIR /app

# 定义挂载卷
VOLUME /opt/services
VOLUME /etc/supervisor/conf.d

# 暴露 Web UI 端口
EXPOSE 9001

# 设置启动脚本
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 设置启动命令
CMD ["/entrypoint.sh"]