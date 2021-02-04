#!/bin/bash

docker build -t gene_data_explorer .
docker start gene_data_mysql
docker run --rm -it --network gene_data_mysql_network -p 5000:80 -v ~/openssl:/root/openssl gene_data_explorer
