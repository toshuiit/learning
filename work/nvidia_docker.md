Configure NVIDIA DOCKER on Ubuntu 22.04
```
apt-get update
apt-get install ca-certificates curl gnupg lsb-release
```
```
mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] 
https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
```
apt-get update
apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```
```
systemctl --now enable docker
```
```
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
 && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
```
```
sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
apt-get update
apt-get install -y nvidia-docker2
```
```
systemctl restart docker
cd /etc/docker/
```
```
vim daemon.json and add following lines.
{
 "runtimes": {
 "nvidia": {
 "path": "nvidia-container-runtime",
 "runtimeArgs": []
 }
 },
 "bip": "192.168.1.1/24"
}
```
```
systemctl daemon-reload
systemctl restart docker
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw enable
ufw allow from 172.27.96.114 to any port 2375
ufw enable
```
