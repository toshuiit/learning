## Download wazuh installation script
```
curl -sO https://packages.wazuh.com/4.5/wazuh-install.sh && sudo bash ./wazuh-install.sh -a
```
## Agent Installation on Ubuntu Client
```
curl -so wazuh-agent.deb https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/wazuh-agent_4.5.4-1_amd64.deb && sudo WAZUH_MANAGER='172.27.15.253' dpkg -i ./wazuh-agent.deb
```
## Start the services
```
sudo systemctl daemon-reload
sudo systemctl enable wazuh-agent
sudo systemctl start wazuh-agent
```
## Wazuh Change Password
```
bash wazuh-passwords-tool.sh -a
```


