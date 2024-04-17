FROM 192.168.50.212/library/java8:v1
ARG CODE_VERSION=v1.0.0
WORKDIR /usr/local
RUN mkdir -p /usr/local/databuff/webapp/
  ## 复制文件并解压
ADD databuff-webapp.jar /usr/local/databuff/webapp/
ADD startWebapp.sh /usr/local/databuff/webapp/
EXPOSE 18080

  ## 执行启动脚本
CMD ["/bin/bash", "/usr/local/databuff/webapp/startWebapp.sh"]