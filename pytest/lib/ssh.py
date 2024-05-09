#!/usr/bin/python3
# -*- coding:utf-8 -*-

import paramiko
import math
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
sys.path.append(BASE_DIR)
from config import sshConfig

class ssh:
    def __init__(self, sshConfig):
        self.address = sshConfig['address']
        self.username = sshConfig['username']
        self.password = sshConfig['password']
        self.default_port = sshConfig['default_port']


    # 初始化,远程模块
    def connect(self):
        try:
            self.ssh_obj = paramiko.SSHClient()
            self.ssh_obj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_obj.connect(self.address, self.default_port, self.username, self.password, timeout=3,
                                 allow_agent=False, look_for_keys=False)
            self.sftp_obj = self.ssh_obj.open_sftp()
        except Exception:
            return False


    # 执行非交互命令
    def exec_cmd(self, command):
        try:
            stdin, stdout, stderr = self.ssh_obj.exec_command(command, timeout=300)
            result = stdout.read().decode('utf-8')
            if len(result) != 0:
                result = str(result).strip()
                result = result.replace("b'", "").replace("'", "").replace('\r', '').replace('\n', '')
                print("=== ssh cmd is: '%s' ===\n" %command + "=== result is: '%s' ===" %result)
                return result
            else:
                return None
        except Exception:
            return None


    # 将远程文件下载到本地
    def download_file(self, remote_path, local_path):
        try:
            self.sftp_obj.get(remote_path, local_path)
            return True
        except Exception:
            return False


    # 将本地文件上传到远程
    def upload_file(self, localpath, remotepath):
        try:
            self.sftp_obj.put(localpath, remotepath)
            return True
        except Exception:
            return False

            
    # 关闭接口
    def close(self):
        try:
            self.sftp_obj.close()
            self.ssh_obj.close()
        except Exception:
            pass


    # 获取文件大小
    def get_file_size(self, file_path):
        ref = self.exec_cmd("du -s " + file_path + " | awk '{print $1}'")
        return ref.replace("\n", "")


    # 判断文件是否存在
    def check_file_exist(self, file_path):
        return self.exec_cmd("[ -e {} ] && echo 'True' || echo 'False'".format(file_path))


    # 获取系统型号
    def get_sys_ver(self):
        return self.exec_cmd("dmesg |sed -n '2p' 2>&1")


    # 检测目标主机存活状态
    def check_alive(self):
        try:
            if self.get_sys_ver() != None:
                return True
            else:
                return False
        except Exception:
            return False


    # 获取文件列表,并得到大小
    def get_file_list(self, path):
        try:
            ref_list = []
            self.sftp_obj.chdir(path)
            file_list = self.sftp_obj.listdir("./")
            for sub_path in file_list:
                dict = {}
                file_size = self.GetFileSize(path + sub_path)
                dict[path + sub_path] = file_size
                ref_list.append(dict)
            return ref_list
        except Exception:
            return False


    # 将远程文件全部打包后拉取到本地
    def download_tar_file(self, path):
        try:
            file_list = self.sftp_obj.listdir(path)
            self.sftp_obj.chdir(path)
            for packageName in file_list:
                self.ssh_obj.exec_command("tar -czf /tmp/{0}.tar.gz {0}".format(packageName))
                self.sftp_obj.get("/tmp/{}.tar.gz".format(packageName), "./file/{}.tar.gz".format(packageName))
                self.sftp_obj.remove("/tmp/{}.tar.gz".format(packageName))
                return True
        except Exception:
            return True


    # 获取磁盘空间并返回字典
    def get_disk_info(self):
        ref_dict = {}
        cmd_dict = {"Linux\n": "df | grep -v 'Filesystem' | awk '{print $5 \":\" $6}'",
                    "AIX\n": "df | grep -v 'Filesystem' | awk '{print $4 \":\" $7}'"
                    }
        try:
            os_version = self.get_sys_ver()
            for version, run_cmd in cmd_dict.items():
                if (version == os_version):
                    # 根据不同版本选择不同的命令
                    os_ref = self.exec_cmd(run_cmd)
                    ref_list = os_ref.split("\n")
                    # 循环将其转换为字典
                    for each in ref_list:
                        # 判断最后是否为空,过滤最后一项
                        if each != "":
                            ref_dict[str(each.split(":")[1])] = str(each.split(":")[0])
            return ref_dict
        except Exception:
            return False


    # 获取系统内存利用率
    def get_mem_info(self):
        cmd_dict = {"Linux\n": "cat /proc/meminfo | head -n 2 | awk '{print $2}' | xargs | awk '{print $1 \":\" $2}'",
                    "AIX\n": "svmon -G | grep -v 'virtual' | head -n 1 | awk '{print $2 \":\" $4}'"
                    }
        try:
            os_version = self.get_sys_ver()
            for version, run_cmd in cmd_dict.items():
                if (version == os_version):
                    # 根据不同版本选择不同的命令
                    os_ref = self.exec_cmd(run_cmd)
                    # 首先现将KB转化为MB
                    mem_total = math.ceil(int(os_ref.split(":")[0].replace("\n", "")) / 1024)
                    mem_free = math.ceil(int(os_ref.split(":")[1].replace("\n", "")) / 1024)
 
                    # 计算占用空间百分比
                    percentage = 100 - int(mem_free / int(mem_total / 100))
                    # 拼接字典数据
                    return {"Total": str(mem_total), "Free": str(mem_free), "Percentage": str(percentage)}
        except Exception:
            return False


    # 获取系统进程信息,并返回字典格式
    def get_process_info(self):
        ref_dict = {}
        cmd_dict = {"Linux\n": "ps aux | grep -v 'USER' | awk '{print $2 \":\" $11}' | uniq",
                    "AIX\n": "ps aux | grep -v 'USER' | awk '{print $2 \":\" $12}' | uniq"
                    }
        try:
            os_version = self.get_sys_ver()
            for version, run_cmd in cmd_dict.items():
                if (version == os_version):
                    os_ref = self.exec_cmd(run_cmd)
                    ref_list = os_ref.split("\n")
                    for each in ref_list:
                        if each != "":
                            ref_dict[str(each.split(":")[0])] = str(each.split(":")[1])
            return ref_dict
        except Exception:
            return False


    # 获取CPU利用率
    def get_cpu_info(self):
        ref_dict = {}
        cmd_dict = {"Linux\n": "vmstat | tail -n 1 | awk '{print $13 \":\" $14 \":\" $15}'",
                    "AIX\n": "vmstat | tail -n 1 | awk '{print $14 \":\" $15 \":\" $16}'"
                    }
        try:
            os_version = self.get_sys_ver()
            for version, run_cmd in cmd_dict.items():
                if (version == os_version):
                    os_ref = self.exec_cmd(run_cmd)
                    ref_list = os_ref.split("\n")
                    for each in ref_list:
                        if each != "":
                            each = each.split(":")
                            ref_dict = {"us": each[0],"sys":each[1],"idea":each[2]}
            return ref_dict
        except Exception:
            return False


    # 获取机器的负载情况
    def get_load_info(self):
        ref_dict = {}
        cmd_dict = {"Linux\n": "uptime | awk '{print $10 \":\" $11 \":\" $12}'",
                    "AIX\n": "uptime | awk '{print $10 \":\" $11 \":\" $12}'"
                    }
        try:
            os_version = self.get_sys_ver()
            for version, run_cmd in cmd_dict.items():
                if (version == os_version):
                    os_ref = self.exec_cmd(run_cmd)
                    ref_list = os_ref.split("\n")
                    for each in ref_list:
                        if each != "":
                            each = each.replace(",","").split(":")
                            ref_dict = {"1avg": each[0],"5avg": each[1],"15avg": each[2]}
                            return ref_dict
            return False
        except Exception:
            return False
 

    # 获取当前系统端口状态数据,只支持Linux
    def get_port_info(self):
        ref_port_list = []
        cmd_dict = {"Linux\n": "netstat -antp | grep -vE '^[^tcp]' | grep -v '::' | awk '{print $4 \":\" $6}'",
                    "AIX\n": "uptime"
                    }
        try:
            os_version = self.get_sys_ver()
            for version, run_cmd in cmd_dict.items():
                if (version == os_version):
                    os_ref = self.exec_cmd(run_cmd)
                    ref_list = os_ref.split("\n")
 
                    for each in ref_list:
                        if each != "":
                            dic = { "Address": each.split(":")[0],"Port": each.split(":")[1],"Status": each.split(":")[2] }
                            ref_port_list.append(dic)
                return ref_port_list
            return False
        except Exception:
            return False
 

    # 修改当前用户密码
    def change_passwd(self,username,password):
        try:
            os_id = self.exec_cmd("id | awk {'print $1'}")
            print(os_id)
            if(os_id == "uid=0(root)\n"):
                self.exec_cmd("echo '{}' | passwd --stdin '{}' > /dev/null".format(password,username))
                return True
        except Exception:
            return False


if __name__ == "__main__":
    print ('This is main of module "ssh.py"')
    s = ssh(sshConfig)
    print(s.check_alive())
    s.connect()
    print(s.check_alive())