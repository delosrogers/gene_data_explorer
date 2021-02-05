#/bin/bash

export FLASK_ENV=development
export FLASK_APP=gene_data_explorer
flask run --host 0.0.0.0 --port 80 --key "/var/ssl/private/${KEY_THUMBPRINT}.p12"
#--cert "/var/ssl/certs/${KEY_THUMBPRINT}.der" 
