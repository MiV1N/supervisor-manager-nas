import os
import sys

def generate_supervisor_conf(services_dir, conf_dir):
    for service_name in os.listdir(services_dir):
        service_path = os.path.join(services_dir, service_name)
        if os.path.isdir(service_path):
            main_py = os.path.join(service_path, 'main.py')
            if os.path.exists(main_py):
                conf_file = os.path.join(conf_dir, f'{service_name}.ini')
                with open(conf_file, 'w') as f:
                    f.write(f'''[program:{service_name}]
command=python {main_py}
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
    generate_supervisor_conf(services_directory, supervisor_conf_directory)