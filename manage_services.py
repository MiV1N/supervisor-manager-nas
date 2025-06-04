import os
import sys
from pathlib import Path

def clean_orphaned_configs(services_dir, conf_dir):
    """清理那些服务目录已不存在但配置文件仍然存在的配置"""
    services_path = Path(services_dir)
    conf_path = Path(conf_dir)
    
    # 获取所有现有的服务目录名称
    existing_services = {d.name for d in services_path.iterdir() if d.is_dir()}
    
    # 获取并处理所有.ini配置文件
    for conf_file in conf_path.glob('*.ini'):
        service_name = conf_file.stem  # 获取不带扩展名的文件名
        if service_name not in existing_services:
            conf_file.unlink()  # 删除文件
            print(f"Removed orphaned config file: {conf_file.name}")

def generate_supervisor_conf(services_dir, conf_dir):
    for service_name in os.listdir(services_dir):
        service_path = os.path.join(services_dir, service_name)
        if os.path.isdir(service_path):
            main_py = os.path.join(service_path, 'main.py')
            if os.path.exists(main_py):

                #虚拟环境存在情况
                venv_path = os.path.join(service_path, 'venv')
                if not os.path.exists(venv_path):  
                    os.system(f'python -m venv {venv_path}')
                    print(f"Created virtual environment for {service_name}")

                # 确定执行器和入口文件路径
                python_path = os.path.join(venv_path, 'bin', 'python')
                command = f'{python_path} {main_py}'

                # requirements.txt依赖安装
                requirements_txt = os.path.join(service_path, 'requirements.txt')
                if os.path.exists(requirements_txt):  
                    os.system(f'{python_path} -m pip install -r {requirements_txt}')
                    print(f"Installed dependencies for {service_name}")

                conf_file = os.path.join(conf_dir, f'{service_name}.ini')
                with open(conf_file, 'w') as f:
                    f.write(f'''[program:{service_name}]
command={command}
directory={service_path}
user=root
autostart=true
autorestart=true
stdout_logfile=/var/log/supervisor/{service_name}.log
stderr_logfile=/var/log/supervisor/{service_name}.err.log
''')
                    print(f"Generated Supervisor config for {service_name}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python manage_services.py <services_directory> <supervisor_conf_directory>")
        sys.exit(1)
    services_directory = sys.argv[1]
    supervisor_conf_directory = sys.argv[2]
    clean_orphaned_configs(services_directory, supervisor_conf_directory)
    generate_supervisor_conf(services_directory, supervisor_conf_directory)