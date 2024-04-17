#!/bin/bash

set -e

HOST=$(hostname -s)
DOMAIN=$(hostname -d)
CLIENT_PORT=2181
SERVER_PORT=2888
ELECTION_PORT=3888

function createConfig(){
    if [[ ! -f "$ZOO_CONF_DIR/${HOST}/zoo.cfg" ]]; then

        mkdir -p $ZOO_CONF_DIR/${HOST}
        mkdir -p $ZOO_DATA_DIR/${HOST}
        mkdir -p $ZOO_DATA_LOG_DIR/${HOST}

        CONFIG="$ZOO_CONF_DIR/${HOST}/zoo.cfg"
        {
            echo "dataDir=$ZOO_DATA_DIR/${HOST}"
            echo "dataLogDir=$ZOO_DATA_LOG_DIR/${HOST}"

            echo "tickTime=$ZOO_TICK_TIME"
            echo "initLimit=$ZOO_INIT_LIMIT"
            echo "syncLimit=$ZOO_SYNC_LIMIT"

            echo "autopurge.snapRetainCount=$ZOO_AUTOPURGE_SNAPRETAINCOUNT"
            echo "autopurge.purgeInterval=$ZOO_AUTOPURGE_PURGEINTERVAL"
            echo "maxClientCnxns=$ZOO_MAX_CLIENT_CNXNS"
            echo "standaloneEnabled=$ZOO_STANDALONE_ENABLED"
            echo "admin.enableServer=$ZOO_ADMINSERVER_ENABLED"
        } >> ${CONFIG}

        if [[ -n $ZOO_4LW_COMMANDS_WHITELIST ]]; then
            echo "4lw.commands.whitelist=$ZOO_4LW_COMMANDS_WHITELIST" >> ${CONFIG}
        fi

        for cfg_extra_entry in $ZOO_CFG_EXTRA; do
            echo "$cfg_extra_entry" >> ${CONFIG}
        done
    fi
}

function getHostNum(){
    if [[ $HOST =~ (.*)-([0-9]+)$ ]]; then
        NAME=${BASH_REMATCH[1]}
        ORD=${BASH_REMATCH[2]}
    else
        echo "Fialed to parse name and ordinal of Pod"
        exit 1
    fi
}

function createID(){
    ID_FILE="$ZOO_DATA_DIR/${HOST}/myid"
    MY_ID=$((ORD+1))
    echo $MY_ID > $ID_FILE
}

function addServer(){
    for (( i=1; i<=$SERVERS; i++ ))
    do
        s="server.$i=$NAME-$((i-1)).$DOMAIN:$SERVER_PORT:$ELECTION_PORT;$CLIENT_PORT"
        [[ $(grep "$s" $ZOO_CONF_DIR/${HOST}/zoo.cfg) ]] || echo $s >> $ZOO_CONF_DIR/${HOST}/zoo.cfg
    done
}

function userPerm(){
    if [[ "$1" = 'zkServer.sh' && "$(id -u)" = '0' ]]; then
        chown -R zookeeper "$ZOO_DATA_DIR" "$ZOO_DATA_LOG_DIR" "$ZOO_LOG_DIR" "$ZOO_CONF_DIR"
        exec gosu zookeeper "$0" "$@"
    fi
}

function startZK(){
    /apache-zookeeper-3.6.2-bin/bin/zkServer.sh --config "$ZOO_CONF_DIR/$(hostname -s)" start-foreground
}

createConfig
getHostNum
createID
addServer
userPerm
startZK