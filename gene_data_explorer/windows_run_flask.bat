cd gene_data_explorer
pip install -r requirements.txt
cd ..
set FLASK_APP=gene_data_explorer
set FLASK_ENV=development
set HOMEDIR=%HOMEDRIVE%%HOMEPATH%
flask run --cert %HOMEDIR%\.openssl\selfsigned.crt --key %HOMEDIR%\.openssl\selfsigned.key