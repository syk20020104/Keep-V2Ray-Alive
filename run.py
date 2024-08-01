import os
import paramiko
import json

def ssh_execute_command(hosts_info, command):
    results = []
    for host_info in hosts_info:
        hostname = host_info['hostname']
        username = host_info['username']
        password = host_info['password']
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=hostname, port=22, username=username, password=password)
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()
            ssh.close()
            if error:
                results.append((hostname, error))
            else:
                results.append((hostname, output))
        except Exception as e:
            print(f"用户：{username}，连接 {hostname} 时出错: {str(e)}")
            results.append((hostname, str(e)))
    return results

ssh_info_str = os.getenv('SSH_INFO', '[]')  # 从环境变量获取SSH信息
hosts_info = json.loads(ssh_info_str)        # 解析JSON格式的SSH信息

# 要执行的命令
command = "pm2 start ./domains/v2ray/v2ray --name v2ray --run"

# 执行命令并获取结果
results = ssh_execute_command(hosts_info, command)
for hostname, result in results:
    print(f"在服务器 {hostname} 上执行命令的结果: {result}")
