#!/bin/bash -e

# Allow specific kafka versions to perform any unique bootstrap operations
OVERRIDE_FILE="/opt/overrides/${KAFKA_VERSION}.sh"
if [[ -x "$OVERRIDE_FILE" ]]; then
    echo "Executing override file $OVERRIDE_FILE"
    eval "$OVERRIDE_FILE"
fi

# Store original IFS config, so we can restore it at various stages
ORIG_IFS=$IFS

if [[ -z "$KAFKA_ZOOKEEPER_CONNECT" ]]; then
    echo "ERROR: missing mandatory config: KAFKA_ZOOKEEPER_CONNECT"
    exit 1
fi

if [[ -z "$KAFKA_PORT" ]]; then
    export KAFKA_PORT=9092
fi

create-topics.sh &
unset KAFKA_CREATE_TOPICS

if [[ -z "$KAFKA_BROKER_ID" ]]; then
    if [[ -n "$BROKER_ID_COMMAND" ]]; then
        KAFKA_BROKER_ID=$(eval "$BROKER_ID_COMMAND")
        export KAFKA_BROKER_ID
    else
        export KAFKA_BROKER_ID=-1
    fi
fi

if [[ -z "$KAFKA_LOG_DIRS" ]]; then
    export KAFKA_LOG_DIRS="/kafka/kafka-logs-$HOSTNAME"
fi

if [[ -n "$KAFKA_HEAP_OPTS" ]]; then
    sed -r -i 's/(export KAFKA_HEAP_OPTS)="(.*)"/\1="'"$KAFKA_HEAP_OPTS"'"/g' "$KAFKA_HOME/bin/kafka-server-start.sh"
    unset KAFKA_HEAP_OPTS
fi

if [[ -n "$HOSTNAME_COMMAND" ]]; then
    HOSTNAME_VALUE=$(eval "$HOSTNAME_COMMAND")

    # Replace any occurences of _{HOSTNAME_COMMAND} with the value
    IFS=$'\n'
    for VAR in $(env); do
        if [[ $VAR =~ ^KAFKA_ && "$VAR" =~ "_{HOSTNAME_COMMAND}" ]]; then
            eval "export ${VAR//_\{HOSTNAME_COMMAND\}/$HOSTNAME_VALUE}"
        fi
    done
    IFS=$ORIG_IFS
fi

if [[ -n "$PORT_COMMAND" ]]; then
    PORT_VALUE=$(eval "$PORT_COMMAND")

    # Replace any occurences of _{PORT_COMMAND} with the value
    IFS=$'\n'
    for VAR in $(env); do
        if [[ $VAR =~ ^KAFKA_ && "$VAR" =~ "_{PORT_COMMAND}" ]]; then
	    eval "export ${VAR//_\{PORT_COMMAND\}/$PORT_VALUE}"
        fi
    done
    IFS=$ORIG_IFS
fi

if [[ -n "$RACK_COMMAND" && -z "$KAFKA_BROKER_RACK" ]]; then
    KAFKA_BROKER_RACK=$(eval "$RACK_COMMAND")
    export KAFKA_BROKER_RACK
fi

if [[ -z "$KAFKA_ADVERTISED_HOST_NAME$KAFKA_LISTENERS" ]]; then
    if [[ -n "$KAFKA_ADVERTISED_LISTENERS" ]]; then
        echo "ERROR: Missing environment variable KAFKA_LISTENERS. Must be specified when using KAFKA_ADVERTISED_LISTENERS"
        exit 1
    elif [[ -z "$HOSTNAME_VALUE" ]]; then
        echo "ERROR: No listener or advertised hostname configuration provided in environment."
        echo "       Please define KAFKA_LISTENERS / (deprecated) KAFKA_ADVERTISED_HOST_NAME"
        exit 1
    fi

    export KAFKA_ADVERTISED_HOST_NAME="$HOSTNAME_VALUE"
fi

echo "" >> "$KAFKA_HOME/config/server.properties"

(
    function updateConfig() {
        key=$1
        value=$2
        file=$3

        echo "[Configuring] '$key' in '$file'"

        if grep -E -q "^#?$key=" "$file"; then
            sed -r -i "s@^#?$key=.*@$key=$value@g" "$file"
        else
            echo "$key=$value" >> "$file"
        fi
    }

    # KAFKA_VERSION + KAFKA_HOME + grep -rohe KAFKA[A-Z0-0_]* /opt/kafka/bin | sort | uniq | tr '\n' '|'

EXCLUSIONS="|KAFKA_VERSION|KAFKA_HOME|KAFKA_DEBUG|KAFKA_GC_LOG_OPTS|KAFKA_HEAP_OPTS|KAFKA_JMX_OPTS|KAFKA_JVM_PERFORMANCE_OPTS|KAFKA_LOG|KAFKA_OPTS|"


    IFS=$'\n'
    for VAR in $(env)
    do
        env_var=$(echo "$VAR" | cut -d= -f1)
        if [[ "$EXCLUSIONS" = *"|$env_var|"* ]]; then
            echo "Excluding $env_var from broker config"
            continue
        fi

        if [[ $env_var =~ ^KAFKA_ ]]; then
            kafka_name=$(echo "$env_var" | cut -d_ -f2- | tr '[:upper:]' '[:lower:]' | tr _ .)
            updateConfig "$kafka_name" "${!env_var}" "$KAFKA_HOME/config/server.properties"
        fi

        if [[ $env_var =~ ^LOG4J_ ]]; then
            log4j_name=$(echo "$env_var" | tr '[:upper:]' '[:lower:]' | tr _ .)
            updateConfig "$log4j_name" "${!env_var}" "$KAFKA_HOME/config/log4j.properties"
        fi
    done

    PODNAME=$(hostname -s | awk -F'-' 'OFS="-"{$NF="";print}' |sed 's/-$//g')
    for ((i=0;i<$SERVERS;i++))
    do
        BOOTSTRAP_SERVERS+="$PODNAME-$i.$(hostname -d):${KAFKA_PORT},"
    done
    BOOTSTRAP_SERVERS=${BOOTSTRAP_SERVERS%?}
    echo ${BOOTSTRAP_SERVERS} > /opt/log.txt
    sed -i "s/bootstrap.servers.*$/bootstrap.servers=$BOOTSTRAP_SERVERS/g" $KAFKA_HOME/config/consumer.properties
    sed -i "s/bootstrap.servers.*$/bootstrap.servers=$BOOTSTRAP_SERVERS/g" $KAFKA_HOME/config/producer.properties
)

if [[ -n "$CUSTOM_INIT_SCRIPT" ]] ; then
  eval "$CUSTOM_INIT_SCRIPT"
fi

exec "$KAFKA_HOME/bin/kafka-server-start.sh" "$KAFKA_HOME/config/server.properties"