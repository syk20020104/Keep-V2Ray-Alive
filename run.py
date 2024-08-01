import paramiko

def ssh_execute_commands(hosts_info, commands):
    results = {}
    for command in commands:
        results[command] = []
        for host_info in hosts_info:
            hostname = host_info.get('hostname', '未知主机')
            username = host_info.get('username', '未知用户名')
            password = host_info.get('password', '未知密码')

            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname, port=4567, username=username, password=password)
                stdin, stdout, stderr = ssh.exec_command(command)
                output = stdout.read().decode().strip()
                error = stderr.read().decode().strip()
                ssh.close()
                if error:
                    results[command].append((hostname, error))
                else:
                    results[command].append((hostname, output))
            except Exception as e:
                print(f"用户：{username}，连接 {hostname} 时出错: {str(e)}")
                results[command].append((hostname, str(e)))
    return results

# 假设hosts_info是直接在脚本中定义的
hosts_info = [
    # {"hostname": "web5.serv00.com", "username": "syk2002", "password": "eaQ4E3J8Pnp40#1$bnxD"}
    {"hostname": "119.112.71.137", "username": "root", "password": "123"}
]

# 定义要执行的命令列表
commands = ["pm2 start ./domains/v2ray/v2ray --name v2ray --run", "uptime"]

# 执行命令并获取结果
results = ssh_execute_commands(hosts_info, commands)

# 打印每个命令的执行结果
for command, command_results in results.items():
    print(f"执行命令 '{command}' 的结果：")
    for hostname, result in command_results:
        print(f"服务器 {hostname} 的结果是: {result}\n")
