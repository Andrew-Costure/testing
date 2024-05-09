# KernelTA

## 安装必需的软件环境
python3.8, JDK1.8+, allure2.24.1, nodejs


## JDK
```
sudo apt install openjdk-17-jdk
```

## nodejs
```
sudo apt install nodejs
```

## allure下载安装步骤
```
wget https://registry.npmjs.org/allure-commandline/-/allure-commandline-2.24.1.tgz

tar -zxvf allure-commandline-2.24.1.tgz -C allure-commandline-2.24.1

sudo ln -s /mnt/cicv/allure-commandline-2.24.1/package/bin/allure /usr/bin/allure

allure --version

```
## 安装Python3依赖包
```
pip3 install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
```

## 执行自动化测试示例
```
pytest  -sv --alluredir report/result testcase/test_arceos.py --clean-alluredir
```

## 生成并打开测试报告
```
allure generate ./report/result -o ./report/html --clean

allure open -h 127.0.0.1 -p 8883 ./report/html
```
## 
