Configure Node Exporter On Client Side for Prometheus

```
wget https://github.com/prometheus/node_exporter/releases/download/v1.3.1/node_exporter-1.3.1.linux-amd64.tar.gz
```
```
tar xvfz node_exporter-*.*-amd64.tar.gz
```
```
cd node_exporter-*.*-amd64
```
```
sudo mv node_exporter-0.18.1.linux-amd64/node_exporter /usr/local/bin/
```
```
sudo useradd -rs /bin/false node_exporter
```
## Now create a file to run node_exporter as a service
```
sudo vim /etc/systemd/system/node_exporter.service
[Unit]
Description=Node Exporter
After=network.target
[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter
[Install]
WantedBy=multi-user.target
```
```
sudo systemctl daemon-reload
sudo systemctl start node_exporter
sudo systemctl status node_exporter
sudo systemctl enable node_exporter
```
