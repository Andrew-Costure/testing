# #!/usr/bin/python3
# # -*- coding:utf-8 -*-

# import os
# import sys
# import subprocess
# from lib.timeout import communicate_with_timeout, TimeoutExpired
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(BASE_DIR)
# sys.path.append(BASE_DIR)


# class cmd:
#     def __init__(self):
#         self.test = 'test'

#     # 执行非交互命令
#     def run_cmd(self, cmd):
#         # print(os.environ)
#         p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#         stdout, stderr = p.communicate()
#         result = ''

#         # 获取输出时注意编码错误
#         try:
#             result = stdout.decode('utf8').strip()
#         except UnicodeError:
#             try:
#                 result = stdout.decode('gbk').strip()
#             except UnicodeError:
#                 result = stdout.decode('ansi').strip()

#         return p.returncode, result


# if __name__ == "__main__":
#     print ('This is main of module "cmd.py"')
#     c = cmd()
#     print(c.test)
#     code, out = c.run_cmd("ls -lt")
#     if code == 0:
#         print('命令执行成功, code = %s, out = %s'  %(code, out))
#     else:
#         print('命令执行失败, code = %s, out = %s'  %(code, out))
#         sys.exit(1)





# class cmd:
#     def __init__(self):
#         self.test = 'test'

#     # 执行非交互命令
#     def run_cmd(self, cmd, timeout=None):
#         p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
#         try:
#             stdout, stderr = communicate_with_timeout(p, timeout=100)
#             result = self.decode_output(stdout)
#         except TimeoutExpired:
#             result = "Command execution timed out"
        
#         return p.returncode, result

#     def decode_output(self, output):
#         try:
#             result = output.decode('utf-8').strip()
#         except UnicodeError:
#             try:
#                 result = output.decode('gbk').strip()
#             except UnicodeError:
#                 result = output.decode('ansi').strip()

#         return result


#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os
import sys
import subprocess
import signal

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
sys.path.append(BASE_DIR)

class cmd:
    def __init__(self):
        self.test = 'test'

    # 执行非交互命令
    def run_cmd(self, cmd):
        # p = None
        try:
            p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout, stderr = p.communicate(timeout=400)
        except Exception as e:
            return -1, "测试发生异常: %s" %str(e)

        result = ''

        # 获取输出时注意编码错误
        try:
            result = stdout.decode('utf8').strip()
        except UnicodeError:
            try:
                result = stdout.decode('gbk').strip()
            except UnicodeError:
                result = stdout.decode('ansi').strip()

        return p.returncode, result