COLUMN_DICT = {
    'baseMean': 'baseMean',
    'log2FoldChange': 'log2FoldChange',
    'lfcSE':'lfcSE',
    'stat':'stat',
    'pvalue':'pvalue',
    'padj':'padj',
    'larry_log2FoldChange':'log2FoldChange',
    'Larry_PValue':'TagwiseDispersionsPValue',
    'Larry_Padj':'TagwiseDispersionsFDRPValueCorrection',
    'vidal_plate':'ceRNAi_Plate',
    'vidal_row':'ceRNAi_Row',
    'vidal_col':'ceRNAi_Col',
    'ahringer_plate':'Plate',
    'ahringer_well':'Well'
}

TABLE_DICT = {
    'Ahringer_RNAi':'Ahringer_RNAi',
    'Vidal_RNAi':'Vidal_RNAi',
    'all_c_elegans_sequences':'all_c_elegans_sequences',
    'cco1_jmjd_RNAseq':'cco1_jmjd_RNAseq',
    'dat1p_tph1p_v_N2':'dat1p_tph1p_v_N2',
    'dat1p_v_N2':'dat1p_v_N2',
    'eps8_RNAi':'eps8_RNAi',
    'genes':'genes',
    'human_genes':'human_genes',
    'human_mito_stress':'human_mito_stress',
    'rab3p_v_N2':'rab3p_v_N2',
    'tph1p_v_N2':'tph1p_v_N2',
}

GENE_TYPE_DICT = {
    'WBID': 'WormBaseID',
    'Name': 'GeneName',
    'Sequence': 'sequence'
}