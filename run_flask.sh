#/bin/bash

export FLASK_ENV=development
export FLASK_APP=gene_data_explorer
if [[ $AZURE=true ]]
then
    flask run --host 0.0.0.0 --port 80
else
    flask run --host 0.0.0.0 --port 80
fi