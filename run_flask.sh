#/bin/bash

export FLASK_ENV=development
export FLASK_APP=gene_data_explorer
flask run --host 0.0.0.0 --port 80 --cert /var/ssl/certs --key /var/ssl/private