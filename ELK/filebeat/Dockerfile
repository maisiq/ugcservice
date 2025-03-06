FROM elastic/filebeat:8.17.0 as filebeat

ARG config_path=/usr/share/filebeat/filebeat.yml

COPY --chmod=444 ./filebeat.yml ${config_path}