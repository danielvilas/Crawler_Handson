#!/bin/bash
# Step 1 – Run MongoDB in Docker
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=root \
  -e MONGO_INITDB_ROOT_PASSWORD=example \
  -v mongo_data:/data/db \
  mongo:8

echo "MongoDB running — connect with:"
echo " docker exec -it mongodb mongosh 'mongodb://root:example@localhost:27017/'"
