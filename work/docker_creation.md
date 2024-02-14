## Create docker container with Nvidia GPUs enabled
```
docker run --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=3,4 \
--shm-size 8G -it -p 10300:22 --name gpu5_3 \
-v /data/username:/data -d  pytorch:v1
```



## For running jupyter notebook

```
docker run --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=9 --shm-size 8G -it -p 8888:8888 -p 10900:22 --name gpu4_9 -v /data/username:/data -d  pytorch:v1
```
