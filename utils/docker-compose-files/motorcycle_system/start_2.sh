sudo rm -rf /dev/shm/kafka/data/
sudo rm -rf /dev/shm/mongodb/data/
sudo mkdir -p /dev/shm/kafka/config/
sudo cp kafka/volume/config/server.properties /dev/shm/kafka/config/
sudo mkdir -p /dev/shm/mongodb/config/
sudo mkdir -p /dev/shm/mongodb/data/
sudo cp mongo/config/mongod.conf.orig /dev/shm/mongodb/config/
docker compose down
docker compose up