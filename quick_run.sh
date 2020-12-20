#!/bin/zsh

cd src
docker build -t gene_data_explorer .
docker run --rm --network gene_data_mysql_network -p 5001:5001 gene_data_explorer