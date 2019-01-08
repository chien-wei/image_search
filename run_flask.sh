#!/usr/bin/env bash
export FLASK_APP=flaskr
export FLASK_ENV=development
export SECRET_KEY=imageisfun
#export MONGODB="mongodb://web:FzdiUSqhRSSJGNAb@cluster-shard-00-00-2e4i9.mongodb.net:27017,cluster-shard-00-01-2e4i9
# .mongodb.net:27017,cluster-shard-00-02-2e4i9.mongodb.net:27017/admin?ssl=true&replicaSet=Cluster-shard-0&authSource=admin"
flask init-db
flask run