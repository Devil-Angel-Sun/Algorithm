import paramiko, json
import pandas as pd

def Connect(ip, username, password, port, command):
    try:
        ssh = paramiko.SSHClient()  # 创建SSH对象
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 允许连接不在know_hosts文件中的主机
        ssh.connect(hostname = ip, port = port, username = username, password = password)  # 连接服务器
        stdin, stdout, stderr = ssh.exec_command(command)
        result_out,result_err = stdout.read(),stderr.read()
        if len(result_err.decode('utf-8')) == 0:
            result_out = result_out.decode('utf-8') # 解码
            result_out = result_out.split('\t')
        else:
            print('错误信息为{}'.format(result_err.decode('utf-8')))
    except Exception as e:
        print('无法连接到当前主机,当前错误为{}'.format(e))
    return result_out    

def Handle_format(result_out):
    result = []
    for i in result_out:
        for j in i.split('\n'):
            if j != '':
                result.append(j)
    return result

def Divide_block(results):
    handle_index = []
    for i in results:
        if i.startswith('Handle'):
            handle_index.append(results.index(i))  
    results_block = Handle_index(results, handle_index)
    return results_block

def Handle_index(result, handle_index):
    # 分阶段处理,将单个硬件的所有信息划分到一起
    results_information = []
    for i in handle_index[:-1]:
        result_information = []
        for j in result[i:handle_index[handle_index.index(i)+1]]:
            result_information.append(j)
        results_information.append(result_information)    
    result_information = []
    for j in result[handle_index[-1]:]:
        result_information.append(j)
    results_information.append(result_information)
    return results_information

def Get_index(results):
    handle_index = []
    for i in results:
        if i.startswith('Handle'):
            handle_index.append(results.index(i))
    return handle_index
    
def Trans_json(results_all, name, ip):
    file_path = './information/{0}_{1}_information.json'.format(ip, name)
    with open(file_path, 'w', encoding = 'utf-8') as f:
        json.dump(results_all, # 待写入数据
                 f, # File对象
                 indent = 2, # 空格缩进符，多行显示；若无该参数，显示数据在一行中显示
                 sort_keys = True, # 键的排序
                 ensure_ascii = False) # 显示中文