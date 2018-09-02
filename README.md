# dalla-stats2
Traffic accounting for TP-LINK AC750 Archer C20 Router 

## Requirements
- Docker

## Deploy
```
docker service create --name registry --publish published=5000,target=5000 registry:2

./build-to-registry.sh

cp config.ini config.local.ini
cp mysql_root_password.txt.keep mysql_root_password.txt

docker stack deploy -c docker-compose.yml dalla-stats
```