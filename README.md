# 数据探查部署文档

------
- [数据探查部署文档](#数据探查部署文档)
  - [项目结构](#项目结构)
  - [离线环境部署数据库jdk](#离线环境部署数据库jdk)
      - [docker 安装](#docker-安装)
      - [离线安装镜像](#离线安装镜像)
      - [离线安装jdk](#离线安装jdk)
  - [python后端部署](#python后端部署)
      - [配置config.yaml](#配置configyaml)
      - [启动程序](#启动程序)
  - [开发环境部署](#开发环境部署)






##  项目结构

```shell
- data-exploration
	- backend
		- database # 数据库实例
		- expand  # 拓展（AI预处理等）
		- llm  # 大模型service
		- routers # 接口信息
		- sql  # sql文件(项目初始化)
		- template # 模板
		- config.yaml # 项目配置文件
	- data_resources  # 历史资源保存路径
	- install_package # docker镜像等中间件
	- scheduler_redis # 定时任务模块
	- data-exploration.tar.gz # 依赖环境包
	- app.py  # 启动文件
	- gunicorn_control.sh # 启动sh文件
	- scheduler_control.sh # 定时任务启动sh文件
```



## 离线环境部署数据库jdk

####  docker 安装

- ```shell
   解压文件
  tar -zxvf docker-20.10.0.tgz
  
   拷贝命令到 /usr/bin 目录下
  cp docker/* /usr/bin/
  ```

  

- 使用 **"vi /usr/lib/systemd/system/docker.service"**命令，把如下信息写入

- ```sh
  
  docker.service
   
  [Unit]
  Description=Docker Application Container Engine
  Documentation=https://docs.docker.com
  After=network-online.target firewalld.service
  Wants=network-online.target
   
  [Service]
  Type=notify
  # the default is not to use systemd for cgroups because the delegate issues still
  # exists and systemd currently does not support the cgroup feature set required
  # for containers run by docker
  ExecStart=/usr/bin/dockerd
  ExecReload=/bin/kill -s HUP $MAINPID
  # Having non-zero Limit*s causes performance problems due to accounting overhead
  # in the kernel. We recommend using cgroups to do container-local accounting.
  LimitNOFILE=infinity
  LimitNPROC=infinity
  LimitCORE=infinity
  # Uncomment TasksMax if your systemd version supports it.
  # Only systemd 226 and above support this version.
  #TasksMax=infinity
  TimeoutStartSec=0
  # set delegate yes so that systemd does not reset the cgroups of docker containers
  Delegate=yes
  # kill only the docker process, not all processes in the cgroup
  KillMode=process
  # restart the docker process if it exits prematurely
  Restart=on-failure
  StartLimitBurst=3
  StartLimitInterval=60s
   
  [Install]
  WantedBy=multi-user.target
  
  
  ```



- ```shell
   执行如下命令
  systemctl daemon-reload
  
   开机自启动设置
  systemctl enable docker
  
   启动docker
  systemctl start docker
  
   验证docker是否安装成功
  docker info
  docker run hello-word
  ```



####  离线安装镜像

- ```shell
   离线安装postgres
   docker加载本地镜像包
  docker load -i postgre16.tar
  
   运行postgres_docker_run.sh
  bash postgres_docker_run.sh
  
   离线安装nginx
   docker加载本地镜像包
  docker load -i nginx.tar
  
   离线安装redis
   docker加载本地镜像包
  docker load -i redis-6.0.8.tar
  
   运行redis6.0.8_run.sh
  bash redis6.0.8_run.sh
  ```



####  离线安装jdk

- ```shell
   解压jdk文件
  tar -zxvf jdk-8u171-linux-x64.tar.gz
  
   增加环境变量
  vi /etc/profile
  
   在文件最底部添加
  export JAVA_HOME=/解压目录/JDK1.8.0_361
  export JRE_HOME=${JAVA_HOME}/jre
  export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
  export PATH=${JAVA_HOME}/bin:$PATH
  
   wq保存后执行
  source /etc/profile
  
   查看版本
  java --version
  ```

  

## python后端部署

####  解压数据探查代码

```bash
# 进入安装目录
cd data-exploration

# 解压依赖环境包
mkdir data-exploration
tar -zxvf data-exploration.tar.gz -C data-exploration

# 进入依赖环境
source data-exploration/bin/activate
```

#### 配置config.yaml

```yaml
# 数据库配置
database:
  host: 192.168.20.48 # 数据库地址
  port: 5432 # 端口
  user: root # 用户名
  password: 123456 # 密码

# 定时任务配置
scheduler:
  thread_num: 20  # 启动线程数量
  process_num: 5 # 启动进程数量
  max_instances: 3 # 最大同时执行数量


```

```shell
# 初始化数据库(后续无需再次运行)
python init_nacos_database.py
```

####  启动程序

```bash
# 进入mian.py所在路径
cd data-exploration
# 运行启动文件
./gunicorn_control
# 查看报错信息
tail -f error.log
# 查看接口响应信息
tail -f access.log
```


##  ORACLE 配置client

```shell
export LD_LIBRARY_PATH=/root/instantclient_12_2:$LD_LIBRARY_PATH
```

