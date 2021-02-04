cd gene_data_explorer
pip install -r requirements.txt
cd ..
set FLASK_APP=gene_data_explorer
set FLASK_ENV=development
set LOGIN_DISABLED=True
set MYSQL_PORT=3306
set HOMEDIR=%HOMEDRIVE%%HOMEPATH%
if %LOGIN_DISABLED% EQU True (
    flask run --no-reload)
else (
    flask run --cert %HOMEDIR%\.openssl\selfsigned.crt --key %HOMEDIR%\.openssl\selfsigned.key
)