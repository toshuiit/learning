GRAFANA AS DOCKER CONTAINER
```
docker volume create grafana-data
```
```
docker volume create grafana-log
```
```
docker volume create grafana-config
```
```
docker run -d --name grafana -p 3000:3000 -v grafana-data:/var/lib/grafana -v grafana-log:/var/log/grafana -v grafana-config:/etc/grafana/ grafana/grafana
```
