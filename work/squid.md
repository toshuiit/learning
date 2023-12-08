## On server side
```
apt install squid
```

## Configure squid on server side
```
vim /etc/squid/squid.conf
http_access allow all
#http_access deny all
```
## Configure client for apt update
```
vim /etc/apt/apt.conf
```
## Add following entries
```
Acquire::http::proxy "http://172.27.15.17:3128/";
Acquire::https::proxy "http://172.27.15.17:3128/";
Acquire::ftp::proxy "http://172.27.15.17:3128/";
```
