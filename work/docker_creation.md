```
docker run --runtime=nvidia -e NVIDIA_VISIBLE_DEVICES=3,4 --shm-size 8G -it \
-p 10300:22 --name gpu5_3 -v /data/username:/data -d  pytorch:v1
```
