#!/bin/bash

java -Xms3G -Xmx3G -Dwebapp.logDir=/usr/local/databuff/webapp/logs -jar /usr/local/databuff/webapp/databuff-webapp.jar --spring.config.location=/usr/local/databuff/webapp/webapp.yml --logging.file=/usr/local/databuff/webapp/logs/databuff-webapp.log