library(tools)

#@ For the gene search to work, you not only need geneIndex.ix file but also
#  geneIndex.ixx file at the file location


files <- list.files("/Library/WebServer/Documents/")
#createBioHTML(files, directory="http://localhost/",type="mouse")
createBioHTML(files)


createBioHTML <- function(allFiles, directory="http://localhost/", type="human") {
  documentHead <- " <!DOCTYPE html>
    <html>
    <head>
    <meta charset=utf-8 />
    <title>Biodalliance</title>
    <head>
    </head>
    <body>
  
    
    <div id=\"title\"> <h1> Genome Browser </h1> 
    </div>
    
    <script language=\"javascript\" src=\"http://www.biodalliance.org/release-0.13/dalliance-compiled.js\"></script>
    <script language=\"javascript\">
    new Browser({ "
  if (type == "human") { 
    Reference <-    "chr: '21',
        viewStart:  33031597,
        viewEnd:  33041570,
        cookieKey: 'human',
        fullScreen: true,
        
        coordSystem: {
          speciesName: 'Human',
          taxon: 9606,
          auth: 'NCBI',
          version: '37',
          ucscName: 'hg19'
        },
        
     sources: [{name: 'Genome',
                twoBitURI:  'http://localhost/hg19.2bit',
                tier_type:  'sequence',
                provides_entrypoints: true,
                pinned: true
               },
               {name: 'GENCODE',
                bwgURI: 'http://localhost/gencode.bb',
                stylesheet_uri: 'http://localhost/gencode.xml',
                collapseSuperGroups: true,
                trixURI: 'http://localhost/geneIndex.ix',
                pinned:true
               }"
  } else {
    Reference <- "chr: '19',
    viewStart:  30000000,
    viewEnd:    30100000,
    cookieKey:  'mouse38',
    fullScreen: true,
    coordSystem: {
      speciesName: 'Mouse',
      taxon: 10090,
      auth: 'GRCm',
      version: 38,
      ucscName: 'mm10' 
    },
      sources:  [{name: 'Genome',
                  twoBitURI:  'http://www.biodalliance.org/datasets/GRCm38/mm10.2bit',
                  desc: 'Mouse reference genome build GRCm38',
                  tier_type: 'sequence',
                  provides_entrypoints: true},
                 {name: 'Genes',
                  desc: 'Gene structures from GENCODE M2',
                  bwgURI: 'http://www.biodalliance.org/datasets/GRCm38/gencodeM2.bb',
                  stylesheet_uri: 'http://www.biodalliance.org/stylesheets/gencode.xml',
                  collapseSuperGroups: true,
                  trixURI: 'http://www.biodalliance.org/datasets/GRCm38/gencodeM2.ix'
                 }"
  }
  
  
  documentEnd <- "]
    });
  </script>
    
    <div id=\"svgHolder\"></div>
    
    </div>
    </body>
    </html>"
  
  formMid <- function(directory, files) {
    tfiles <- files[file_ext(files) %in% c("bw","bam")]
    vcf <- files[file_ext(files) %in% "gz"]
    temp <- sapply(tfiles, function(x) {
      name <- paste(",{name: '",x,"',",sep="")
      collapse <- ifelse(grepl("bw",x),"collapseSuperGroups:true,","")
      URI <- paste(ifelse(grepl("bw",x),"bwgURI: '","bamURI: '"),directory,x,"'}",sep="")
      return (c(name,collapse,URI))
    })
    vcflines <- sapply(vcf, function(s) {
      name <- paste(",{name: '",s,"',",sep="")
      URI <- paste("uri: '",directory,s,"',",sep="")
      tier <- "tier_type: 'tabix',"
      pay <- "payload: 'vcf'}"
      return (c(name,URI,tier,pay))
    })
    return (c(temp,vcflines))
  }
  documentMid<- formMid(directory,allFiles)
  biodalliance <- file("biodalliance.html")
  writeLines(c(documentHead,Reference,documentMid,documentEnd),biodalliance)
  close(biodalliance)
}