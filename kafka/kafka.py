version: '3.1'

networks:
  cdc-network:
    name: cdc-network
    driver: bridge

services:
  zookeeper:
    container_name: zookeeper
    image: docker.io/bitnami/zookeeper:3.8
    ports:
      - "2181:2181"
    volumes:
      - "zookeeper_data:/bitnami"
    environment:
      - ALLOW_ANONYMOUS_LOGIN=yes # You have set the environment variable ALLOW_ANONYMOUS_LOGIN=yes. For safety reasons, do not use this flag in a production environment
  kafka:
    container_name: kafka  
    image: docker.io/bitnami/kafka:3.3
    ports:
      - "9092:9092"
      - '9093:9093'
    depends_on:
      - zookeeper
    volumes:
      - "kafka_data:/bitnami"
    environment:
      # - KAFKA_BROKER_ID=1
      - KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper:2181
      - ALLOW_PLAINTEXT_LISTENER=yes # For safety reasons, do not use this flag in a production environment.
      - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=INSIDE:PLAINTEXT,OUTSIDE:PLAINTEXT
      - KAFKA_CFG_LISTENERS=INSIDE://:9092,OUTSIDE://:9093
      - KAFKA_CFG_ADVERTISED_LISTENERS=INSIDE://kafka:9092,OUTSIDE://<ip_address_where_kafka_is_located>:9093
      - KAFKA_CFG_INTER_BROKER_LISTENER_NAME=INSIDE
      - KAFKA_CFG_AUTO_CREATE_TOPICS_ENABLE=true
  init-kafka:
    container_name: init-kafka
    image: confluentinc/cp-kafka:6.1.1
    depends_on:
      - kafka
    entrypoint: [ '/bin/sh', '-c' ]
    command: |
      "
      # blocks until kafka is reachable
      kafka-topics --bootstrap-server kafka:9092 --list

      # echo -e 'Creating kafka topics....'
      # kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists --topic person --replication-factor 1 --partitions 1
      kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists --topic connect-configs --replication-factor 1 --partitions 1 --config cleanup.policy=compact
      kafka-topics --bootstrap-server kafka:9092 --create --if-not-exists --topic connect-offsets --replication-factor 1 --partitions 25 --config cleanup.policy=compact --config min.cleanable.dirty.ratio=0.001 --config segment.ms=5000

      # echo -e 'Successfully created the following topics:'
      kafka-topics --bootstrap-server kafka:9092 --list
      "
  kafka-connect:
    container_name: kafka-connect
    image: debezium/connect
    ports:
      - "8083:8083"
    environment:
      - GROUP_ID=group-id-nih-bos
      - CONFIG_STORAGE_TOPIC=connect-configs
      - OFFSET_STORAGE_TOPIC=connect-offsets
      - BOOTSTRAP_SERVERS=kafka:9092
    depends_on:
      - kafka
volumes:
  zookeeper_data:
    driver: local
  kafka_data:
    driver: local
