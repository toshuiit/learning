## DNS Preparation for mailcow

* domain: example.iitk.ac.in  
* Set hostname of server to mail.example.iitk.ac.in  
* Add A record for mail.example.iitk.ac.in in DNS  
* Add MX record for domain example.iitk.ac.in to mail.example.iitk.ac.in  
* CNAME record for the subdomains "autodiscover" as well as "autoconfig" and destination must point to mail.example.iitk.ac.in  
* Add an TXT record for your domain and set the value to "v=spf1 mx ~all", to allow the server specified in the MX record (the mail server where Mailcow will be installed) to send e-mails with your domain as the sender domain.  
* Now define the PTR record for mail.example.iitk.ac.in

## Update packages
```
apt update -y && apt upgrade -y
apt dist-upgrade -y
```

## To secure system from brute force attacks
```
apt install fail2ban -y 
```

## Install firewall
```
apt install ufw -y
ufw default deny incoming
ufw default allow outgoing
ufw allow 22,25,80,110,143,443,465,587,993,995,4190/tcp
systemctl enable ufw
systemctl restart ufw
```

## Install mailcow
```
apt update
apt upgrade -y
apt install curl nano git apt-transport-https ca-certificates gnupg2 software-properties-common -y
```

## Add key for docker repo
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```
## Add repo to install docker
```
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list
```
## Update package list and install docker
```
apt update
apt install docker-ce docker-ce-cli -y
```

## Install docker compose
```
curl -L https://github.com/docker/compose/releases/download/v$(curl -Ls https://www.servercow.de/docker-compose/latest.php)/docker-compose-$(uname -s)-$(uname -m) > /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```
## Now go to opt directory
```
cd /opt
```
## Clone the master branch for mailcow
```
git clone https://github.com/mailcow/mailcow-dockerized
cd mailcow-dockerized
./generate_config.sh  # Enter mail.example.iitk.ac.in

Type 1 for master branch selection

Configuration file is created with name mailcow.conf
 "SKIP_LETS_ENCRYPT" to "y" as i have certificates.
```

## Download required images for mailcow
```
docker-compose pull
docker-compose up -d
```
## For HTTP --> HTTPS
vim /opt/mailcow-dockerized/data/conf/nginx/redirect.conf and add given content
```
server {
  root /web;
  listen 80 default_server;
  listen [::]:80 default_server;
  include /etc/nginx/conf.d/server_name.active;
  if ( $request_uri ~* "%0A|%0D" ) { return 403; }
  location ^~ /.well-known/acme-challenge/ {
    allow all;
    default_type "text/plain";
  }
  location / {
    return 301 https://$host$uri$is_args$args;
  }
}
```
## Restart the container
```
docker-compose restart nginx-mailcow
```
## Open URL
https://mail.example.iitk.ac.in
Credentials: admin/moohoo
* Go to System --> Configuration and change password

* An update script in your mailcow-dockerized directory will take care of updates.

* Run the update script in case you need to update:
```
./update.sh
```
