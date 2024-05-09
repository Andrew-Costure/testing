#!/usr/bin/python3
# -*- coding:utf-8 -*-

import subprocess
import os

cur_path = os.path.dirname(os.path.realpath(__file__))

class adb(object):
    def __int__(self, device_id, local_path=cur_path, device_path="sdcard", packname="", grammar="ls", times=1,
                video_name="demo",
                new_tcp=5000, old_tcp=8000, text="default",
                new_x=1, new_y=1, old_x=2, old_y=2, keyevent="home", **kwargs):
        """

        :param device_id: 设备ID
        :param local_path: 本地路径
        :param device_path: 设备路径
        :param packname: 包名
        :param grammar: 语法
        :param times: 时间
        :param video_name: 名字
        :param new_tcp: 新的ip
        :param old_tcp: 当前ip
        :param text: 文本
        :param new_x: 期望坐标x
        :param new_y: 期望坐标y
        :param old_x: 当前坐标x
        :param old_y: 当前坐标y
        :param keyevent: 设备按键
        :return:
        """
        self.devoce_id = device_id
        self.local_path = local_path
        self.device_path = device_path
        self.packname = packname
        self.grammar = grammar
        self.times = times
        self.video_name = video_name
        self.new_tcp = new_tcp
        self.old_tcp = old_tcp
        self.text = text
        self.new_x = new_x
        self.new_y = new_y
        self.old_x = old_x
        self.old_y = old_y
        self.keyevent = keyevent


    @classmethod
    def get_device(cls):
        """
        查看连接设备
        :return:
        """
        devices = os.popen(r"adb devices")
        # print(devices.read())
        return devices.read()


    def get_state(self):
        """
        获取设备状态
        :return:
        """
        out, info = subprocess.getstatusoutput("adb -s {} get-stat".format(self.devoce_id))
        print(out, info)
        return info


    def adb_push(self):
        """
        向设备中复制文件
        :return:
        """
        push = os.popen(r"adb -s {} push {}".format(self.devoce_id, self.local_path, self.device_path))
        print(push.read())
        return push.read()


    def adb_pull(self):
        """
        从设备中复制文件
        :return:
        """
        pull = os.popen(r"adb -s {} push  {}".format(self.devoce_id, self.device_path, self.local_path))
        print(pull.read())
        return pull.read()


    def adb_install(self):
        """
        adb 安装apk
        :return:
        """
        install = os.popen(r"adb -s {} install  {}".format(self.devoce_id, self.packname))
        print(install.read())
        return install.read()


    def adb_uninstall(self):
        """
        adb 卸载apk
        :return:
        """
        uninstall = os.popen(r"adb -s {} uninstall  {}".format(self.devoce_id, self.packname))
        print(uninstall.read())
        return uninstall.read()


    def adb_root(self):
        """
        设备root权限
        :return: root == 0 执行成功返回0
        """
        root = subprocess.call("adb -s {} root".format(self.devoce_id), shell=True)
        print(root)
        return root


    def adb_remount(self):
        """
        给设备读写权限
        :return: remount succeeded
        """
        remount = os.popen("adb -s {} remount".format(self.devoce_id))
        return remount.read()


    def adb_shell(self):
        """
        out是执行成功返回0
        info是执行后控制面板输出
        :return:
        """
        out, info = subprocess.getstatusoutput("adb -s {} shell {}".format(self.devoce_id, self.grammar))
        print(out, info)
        return out, info


    def adb_video(self):
        """
        录制30秒视频
        :return:
        """
        video = subprocess.call("adb shell screenrecord --time-limit {}.mp4 ".format(self.times, self.device_path,
                                                                                     self.video_name),
                                shell=True)
        print(video)
        return video


    def adb_forward(self):
        """
        adb forward tcp:5555 tcp:8000 #设置端口
        :return:
        """

        forward = subprocess.call("adb forward tcp:{} tcp:{}".format(self.old_tcp, self.new_tcp), shell=True)
        print(forward)
        return forward


    def adb_input_text(self):
        """
        # adb  shell  text #该命令主要是用于向获得焦点的EditText控件输入内容，
        :return:
        """
        input_text = subprocess.call("adb  shell  text {}".format(self.text), shell=True)
        print(input_text)
        return input_text


    def adb_input_keyevent(self):
        """
        # adb input keyevent # 该命令主要是向系统发送一个按键指令，实现模拟用户在键盘上的按键动作
        :return:
        """
        input_keyevent = subprocess.call("adb input keyevent {}".format(self.keyevent), shell=True)
        print(input_keyevent)
        return input_keyevent


    def adb_touch(self):
        """
        adb shell input tap #该命令是用于向设备发送一个点击操作的指令，参数是<x> <y>坐标
        :return: 0
        """
        touch = subprocess.call("adb input tap {}".format(self.new_x, self.new_y), shell=True)
        print(touch)
        return touch


    def adb_input_swipe(self):
        """
        # input swipe [duration(ms)]
        # 向设备发送一个滑动指令，并且可以选择设置滑动时长。
        # //滑动操作
        # adb shell input swipe 100 100 200 200  300 //从 100 100 经历300毫秒滑动到 200 200
        # //长按操作
        # adb shell input swipe 100 100 100 100  1000 //在 100 100 位置长按 1000毫秒
        :return: 0
        """
        input_swipe = subprocess.call("adb input swipe {}".format(self.old_x, self.old_y, self.new_x, self.new_y,
                                                                  self.times), shell=True)
        print(input_swipe)
        return input_swipe


    def adb_am_start(self, input_Activity):
        """
         # adb shell am start -n 包名/包名＋类名（-n 类名,-a action,-d date,-m MIME-TYPE,-c category,-e 扩展数据,等）
         # 启动Activity
        :param input_Activity:
        :return:
        """
        am_start = subprocess.call("adb -s {} shell am start {}".format(self.devoce_id, input_Activity), shell=True)
        print(am_start)
        return am_start


    def adb_connect(self, host, port):
        """
        connect <host>[:<port>]       - connect to a device via TCP/IP
                                 Port 5555 is used by default if no port number is specified.
        :param host: host
        :param port: port
        :return:
        """
        connect = subprocess.call("adb -s {} connect {}".format(self.devoce_id, host, port), shell=True)
        return connect


    def adb_disconnect(self, host, port):
        """
        disconnect [<host>[:<port>]]  - disconnect from a TCP/IP device.
                                 Port 5555 is used by default if no port number is specified.
                                 Using this command with no additional arguments
                                 will disconnect from all connected TCP/IP devices.
        :param host:
        :param port:
        :return:
        """
        disconnect = subprocess.call("adb -s {} disconnect {}".format(self.devoce_id, host, port), shell=True)
        return disconnect


    def adb_version(self):
        """
        获取adb版本
        :return:
        """
        out, info = subprocess.getstatusoutput("adb version")
        return out, info


    def adb_start_server(self):
        """
        ensure that there is a server running
        :return:
        """
        start_server = subprocess.call("adb start-server  ", shell=True)
        return start_server


    def adb_kill_server(self):
        """
        kill the server if it is running
        :return:
        """
        kill_server = subprocess.call("adb start-server  ", shell=True)
        return kill_server


    def adb_get_state(self):
        """
           - prints: offline | bootloader | device
           :return:
           """
        out, info = subprocess.getstatusoutput("adb state")
        return out, info


    def get_serialno(self):
        """
           - prints: <serial-number>
           :return:
           """
        out, info = subprocess.getstatusoutput("adb get-serialno")
        return out, info


    def get_remount(self):
        """
             - remounts the /system and /vendor (if present) partitions on the device read-write
           :return:
           """
        out, info = subprocess.getstatusoutput("adb remount")
        return out, info


    def adb_reboot(self):
        """
         reboots the device, optionally into the bootloader or recovery program
           :return:
           """
        reboot = subprocess.call("adb -s {} shell reboot ".format(self.devoce_id), shell=True)
        return reboot


if __name__ == '__main__':
    adb = adb(device_id="TNS000000044200002fd")
    adb.adb_root()

