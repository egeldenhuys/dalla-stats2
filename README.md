# dalla-stats2
Traffic accounting for TP-LINK AC750 Archer C20 Router 

## Requirements
- Docker

## Deploy
```
sudo sudo docker run -d -p 127.0.0.1:5000:5000 --restart=always --name registry registry:2

./build-to-registry.sh

cp config.ini config.local.ini
cp mysql_root_password.txt.keep mysql_root_password.txt

docker stack deploy -c docker-compose.yml dalla-stats
```