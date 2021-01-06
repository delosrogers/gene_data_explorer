CREATE TABLE `tmp_all_gene_ids` (
  `unknown` INT NULL,
  `WormBaseID` VARCHAR(45) NOT NULL,
  `gene_name` VARCHAR(255) NULL,
  `Sequence_name` VARCHAR(255) NULL,
  `live` VARCHAR(45) NULL,
  `type` VARCHAR(45) NULL,
  PRIMARY KEY (`WormBaseID`))
ENGINE = InnoDB;

Load data local infile '/Users/mattias/Downloads/c_elegans.PRJNA13758.WS279.geneIDs.txt' INTO TABLE `tmp_all_gene_ids` 
	Columns Terminated by ','
    Lines Terminated By '\n';
    
UPDATE tmp_all_gene_ids INNER JOIN genes ON genes.WormBaseID = tmp_all_gene_ids.WormBaseID SET tmp_all_gene_ids.gid = genes.gid WHERE genes.WormBaseID = tmp_all_gene_ids.WormBaseID;

UPDATE genes INNER JOIN tmp_all_gene_ids USING (gid) SET 
	genes.WormBaseID = tmp_all_gene_ids.WormBaseID,
    genes.GeneName = tmp_all_gene_ids.gene_name,
    genes.sequence = tmp_all_gene_ids.Sequence_name,
    genes.live = tmp_all_gene_ids.live,
    genes.`type` = tmp_all_gene_ids.type,
    genes.`source` = 'WB279 csv of all genes downloaded from ftp site';