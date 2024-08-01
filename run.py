import os
import paramiko
import json

def ssh_execute_commands(hosts_info, commands):
    overall_results = {}
    for command in commands:
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
                    results.append((hostname, command, error))
                else:
                    results.append((hostname, command, output))
            except Exception as e:
                print(f"用户：{username}，连接 {hostname} 时出错: {str(e)}")
                results.append((hostname, command, str(e)))
        overall_results[command] = results
    return overall_results

ssh_info_str = os.getenv('SSH_INFO', '[]')  # 从环境变量获取SSH信息
hosts_info = json.loads(ssh_info_str)        # 解析JSON格式的SSH信息

# 要执行的命令列表
commands = ["cd /usr/home/syk2002/domains/v2ray/v2ray && pwd", "cd domains/v2ray/v2ray && pwd && pm2 start ./v2ray --name my-v2ray -- run"]

# 执行命令并获取结果
results = ssh_execute_commands(hosts_info, commands)

# 打印每个命令的执行结果
for command, command_results in results.items():
    print(f"执行命令 '{command}' 的结果：")
    for hostname, command_executed, result in command_results:
        print(f"服务器 {hostname} 上执行 '{command_executed}' 的结果是: {result}\n")
