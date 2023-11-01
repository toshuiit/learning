## Create portainer docker container
```
docker run -d -p 8000:8000 -p 443:9443 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v /etc/ssl/certs/portainer:/certs -v /data/portainer:/data portainer/portainer-ce:latest --ssl --sslcert /certs/fullchain.pem --sslkey /certs/privkey.pem
```
##For connecting Portainer to Docker hosts follow these steps:
vim /etc/systemd/system/docker.service.d/docker.conf
```
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock
```
##Reload the systemd daemon:
```
systemctl daemon-reload
```
##Restart docker:
```
 systemctl restart docker.service
```
