#/bin/bash

export FLASK_ENV=development
export FLASK_APP=gene_data_explorer

flask run --host 0.0.0.0 --cert ~/openssl/cert.pem --key ~/openssl/key_unencrypted.pem