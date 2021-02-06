#!/bin/bash
. gene_data_explorer/.env
docker build -t gene_data_explorer .
docker start gene_data_mysql
docker run --rm -it --network gene_data_mysql_network -p 5000:80 -v ~/openssl:/root/openssl \
-e GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID} -e GOOGLE_CLIENT_SECRET=${GOOGLE_CLIENT_SECRET} \
-e AZURE_SQL_PASSWD=${AZURE_SQL_PASSWD} -e AZURE_SQL_USERNAME=${AZURE_SQL_USERNAME} -e LOGIN_DISABLED=True gene_data_explorer
