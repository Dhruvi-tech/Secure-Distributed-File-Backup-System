# EFK Logging Stack

Run logging services Elasticsearch, Fluentd, Kibana independently if needed.

docker-compose -f ../cloud/docker-compose.yml up -d fluentd elasticsearch kibana
docker-compose -f ../cloud/docker-compose.yml down

text
