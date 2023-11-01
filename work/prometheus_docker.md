## Prometheus as Docker container

sudo vim /data/prometheus/prometheus.yml
```
# my global config
global:
 scrape_interval: 15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
 evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
 # scrape_timeout is set to the global default (10s).
# Alertmanager configuration
alerting:
 alertmanagers:
 - static_configs:
 - targets:
 # - alertmanager:9093
# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
 # - "first_rules.yml"
 # - "second_rules.yml"
# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
 # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
 - job_name: "prometheus"
 # metrics_path defaults to '/metrics'
 # scheme defaults to 'http'.
 static_configs:
 - targets: 
["localhost:9090","gpu0.cse.iitk.ac.in:9100","gpu1.cse.iitk.ac.in:9100","gpu0.cse.iitk.ac.in:9835","gpu1.cse.iitk.ac.in:98
35","gpu2.cse.iitk.ac.in:9835","gpu2.cse.iitk.ac.in:9100","gpu3.cse.iitk.ac.in:9835","gpu3.cse.iitk.ac.in:9100","gpu4.cse
.iitk.ac.in:9835","gpu4.cse.iitk.ac.in:9100","gpu5.cse.iitk.ac.in:9835","gpu5.cse.iitk.ac.in:9100","image.cse.iitk.ac.in:91
00","image1.cse.iitk.ac.in:9100","image2.cse.iitk.ac.in:9100"]
 - job_name: 'snmp_exporter'
 scrape_interval: 120s
 scrape_timeout: 120s
 static_configs:
 - targets: ['172.25.96.1']
 metrics_path: /snmp
 params:
 module: [if_mib]
 relabel_configs:
 - source_labels: [__address__]
 target_label: __param_target
 - source_labels: [__param_target]
 target_label: instance
 - target_label: __address__
 replacement: 172.27.96.183:9116
```
```
docker run -d --name=prometheus -p 9090:9090 -v /data/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus --config.file=/data/prometheus/prometheus.yml
```
