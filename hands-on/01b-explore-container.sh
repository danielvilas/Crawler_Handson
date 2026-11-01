#!/usr/bin/env bash
# Hands-On 01b — Peek inside the MongoDB container
# Run these commands from your host terminal.

# Open an interactive shell inside the running container
docker exec -it mongodb bash

# ---- Once inside the container ----------------------------------------

# What OS is this container?
cat /etc/os-release

# MongoDB stores its data files here (mounted from the host volume)
ls -lh /data/db

# Environment variables injected with -e at docker run
env | grep MONGO

# Running processes — you should see only mongod (PID 1)
ps aux

# Open the MongoDB shell from inside the container
mongosh -u root -p example

# Leave the shell session (container keeps running)
exit
