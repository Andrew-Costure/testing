# Github码仓接入JenkinsCI配置流程
```
1. Github码仓新增Jenkinsfile文件，内容格式参考：
     <> https://github.com/kraigyang/driver_display/blob/main/Jenkinsfile  (Notes: environment环境变量根据实际情况做修改)

2. Github端配置（Web页面：https://github.com/kern-crates/${repo}）：
     <> Repo Left Settings -> Webhooks -> Payload URL:http://49.51.192.19:9095/github-webhook/ -> Send me everything -> 保存
     <> Repo Right Settings -> Developer Settings -> Personal access tokens -> Tokens(classic) -> Generate -> 保存

3. Jenkins端配置（Web页面：http://49.51.192.19:9095）：
     <> Dashboard -> 系统管理 -> 凭据 -> 系统 -> 全局凭据 (unrestricted) -> Secret Text -> 填入上步中Generate的Token -> ID命名为"GithubAccessToken"（示例） -> 保存
     <> Pipeline -> Configuration -> 构建触发器（Github hook trigger for GITScm polling）-> 流水线（Pipeline script from SCM） -> Add CI monitored repo1/credentials1 -> Add CI monitored related repo2/credentials2 -> 保存

```
# JenkinsCI容器Dockerfile
```
# 基于现有的 Jenkins 镜像
FROM henshing/jenkins_saved:v3

# 切换到 root 用户
USER root

# 生成自定义启动脚本
RUN printf '#!/bin/bash\n# 启动 Jenkins\nexec java -jar -DJENKINS_HOME=/home/jenkins_home /usr/share/jenkins/jenkins.war' > /usr/local/bin/jenkins.sh

# 确保启动脚本具有执行权限
RUN chmod +x /usr/local/bin/jenkins.sh

# 打印启动脚本内容
RUN cat /usr/local/bin/jenkins.sh

# 切换回 Jenkins 用户
USER jenkins

# 设置启动命令
ENTRYPOINT ["/usr/local/bin/jenkins.sh"]
```

# JenkinsCI容器启动流程
```
# [image build]
sudo docker build -t cicv/cicv_jenkins:v1 .
#Notes: 在Dockerfile所在目录执行

# [container start]
sudo docker run -d --privileged -u root --name cicv_jenkins -p 9095:8080 -p 60000:50000 -v /home/jenkins_home:/home/jenkins_home -v /etc/localtime:/etc/localtime cicv/cicv_jenkins:v1
#Notes:  映射端口号9095和60000根据实际环境进行配置
```


# v1.0仓库位置
https://github.com/buhenxihuan/Starry


# 整体流程描述
github action目前在仓库发生push和pr时会自动触发，同时每个四个小时会定时触发，aciton触发后，也可以手动触发，按照auto_test.yml中的流程，先检出整个仓库的代码到aciton的机器中，而后进行前期环境准备，完成后调用pytest和allure进行测试并收集报告，最后通过allure将报告发送到github pages中进行展示。

# auto_test.yml的流程见相应注释 
https://github.com/buhenxihuan/Starry/blob/x86_64/.github/workflows/auto_test.yml

# pytest和allure作用
pytest目录中 config.py文件为pytest执行时读取的配置文件，其中按照类别分别定义了clippy测试的配置，unikernel测试的配置，monolithic测试配置以及一些需要在报告中展示的信息

关键代码为pytest/testcase目录下的test_arceos.py中的代码，具体作用请参见pytest的使用说明（https://learning-pytest.readthedocs.io/zh/latest/index.html ），简单来说就是通过pytest封装了原先从build_img.sh到make执行的过程，全部交由pytest和allure进行接管，从而可以方便的进行结果的收集与过滤

# v1.0使用方法

1. 将auto_test.yml放入.github/workflows(不存在则新建该目录)目录中
2. 将pytest目录放入顶层目录下
3. 向顶层Makefile中加入以下两行
```shell
TC ?= busybox
export AX_TC=$(TC)
```
4. 确保apps目录下有微内核和宏内核测例的入口
5. 选择push、pr、定时或手动触发
6. 若要在线查看报告，请使用github pages进行搭建（具体方法参照 https://docs.github.com/zh/pages/getting-started-with-github-pages/creating-a-github-pages-site ），在auto_test.yml中定义了一个github pages的分支名为gh-pages_ci，若要更改，请查找该文件中的gh-pages_ci字段自行进行替换
7. 一个可以查看的示例 https://buhenxihuan.github.io/Starry/
