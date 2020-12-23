#!/bin/bash
while true
do
curl -X POST -F 'download_type=html' -F 'dataset=tph1p_v_N2' -F 'dataset=dat1p_v_N2' -F 'column=log2FoldChange' -F 'column=padj' -F 'return_missing=False'  -F 'additional_params=tph1p_v_N2.padj < 0.05' localhost:80 
done
