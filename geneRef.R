##HCSC genes, delete all replicates.  Only display the gene once (But getting rid of exons and strand direction)

genes <- read.table("...Your reference file here...")
newG <- genes[!duplicated(genes[c(1,4)]),]

write.table(newG, "refGenes.bed",sep="\t",quote=FALSE,row.names=FALSE)
read.table("refGenes.bed")

