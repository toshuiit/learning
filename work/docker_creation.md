## Create docker container with Nvidia GPUs enabled
```
docker run --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=3,4 \
--shm-size 8G -it -p 10300:22 --name gpu5_3 \
-v /data/username:/data -d  pytorch:v1
```



## For running jupyter notebook

```
docker run -d -p 8000:8000 -p 443:9443 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v /data/portainer:/data portainer/portainer-ce:latest
```