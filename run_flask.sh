#/bin/bash

export FLASK_ENV=development
export FLASK_APP=gene_data_explorer
openssl pkcs12 -in /var/ssl/private/${KEY_THUMBPRINT}.p12 -out /var/ssl/key -nocerts -nodes
openssl pkcs12 -in /var/ssl/private/${KEY_THUMBPRINT}.p12 -out /var/ssl/cert -clcerts -nokeys
flask run --host 0.0.0.0 --port 80 --cert /var/ssl/cert --key "/var/ssl/key"
#--cert "/var/ssl/certs/${KEY_THUMBPRINT}.der" 
