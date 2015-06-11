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
  new Browser({
    chr:          '21',
    viewStart:    33031597,
    viewEnd:      33041570,
    cookieKey:    'human',
    fullScreen: true,
    
    coordSystem: {
      speciesName: 'Human',
      taxon: 9606,
      auth: 'NCBI',
      version: '37',
      ucscName: 'hg19'
    },
    
    sources:     [ {name:  'Genome',
 twoBitURI:  'http://localhost/hg19.2bit',
 tier_type:  'sequence',
 provides_entrypoints: true,
 pinned: true
},

{name: 'GENCODE',
 bwgURI: 'http://localhost/gencode.bb',
 stylesheet_uri: 'http://www.biodalliance.org/stylesheets/gencode.xml',
 collapseSuperGroups: true,
 trixURI: 'http://www.biodalliance.org/datasets/geneIndex.ix',
 pinned:true}"

documentEnd <- "]
  });
</script>
  
  <div id=\"svgHolder\"></div>
  
  </div>
  </body>
  </html>"


files <- list.files("/Library/WebServer/Documents/")

formMid <- function(directory, files) {
  temp <- sapply(files, function(x) {
    name <- paste(",{name: '",x,"',",sep="")
    collapse <- ifelse(grepl("bw",x),"collapseSuperGroups:true","")
    URI <- paste(ifelse(grepl("bw",x),"bwgURI: '","bamURI: '"),directory,x,"'}",sep="")
    return (c(name,collapse,URI))
  })
  return (temp)
}
documentMid<- formMid("http://localhost/",files)

biodalliance <- file("biodalliance.html")
writeLines(c(documentHead,documentMid,documentEnd),biodalliance)
close(biodalliance)
s