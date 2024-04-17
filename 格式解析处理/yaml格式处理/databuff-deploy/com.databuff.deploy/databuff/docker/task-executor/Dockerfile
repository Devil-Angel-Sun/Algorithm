FROM 192.168.50.212/library/java8:v1
ARG CODE_VERSION=v1.0.0
WORKDIR /usr/local
RUN mkdir -p /usr/local/databuff
  ## 复制文件并解压
ADD task-executor.tar /usr/local/databuff/
EXPOSE 18089
EXPOSE 9999
  
  ## 执行启动脚本
CMD ["/bin/bash", "/usr/local/databuff/task-executor/bin/startTaskExecutor.sh"]