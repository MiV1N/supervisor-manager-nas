#!/bin/bash
# python /app/manage_services/manage_services.py /opt/services /etc/supervisor/conf.d
# /usr/local/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf -n  #添加-n在前台运行，后台运行前台进程结束，会被docker认为容器进程退出。
echo "Executing entrypoint.sh"
echo "Running manage_services.py..."
python /app/manage_services/manage_services.py /opt/services /etc/supervisor/conf.d
echo "manage_services.py finished with exit code: $?"
echo "Starting supervisord..."
/usr/local/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf -n
echo "supervisord exited with code: $?"