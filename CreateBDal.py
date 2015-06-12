import string
import os
#files=next(os.walk("/Library/WebServer/Documents/"))[2]
def creatBioHTML(allFiles, URL="http://localhost", type="human"):
	f = open('test.html','w')
	documentHead = """ 
<!DOCTYPE html>
	<html>
	<head>
		<meta charset=utf-8 />
		<title>Biodalliance</title>
		<head>
	</head>
	<body>
		<div id="title"> <h1> Genome Browser </h1> 
	</div>
		
	<script language="javascript" src="%s/biodalliance.js"></script> 
	<script language="javascript">
		new Browser({ """% URL

	taxon = (type=="human") and '9606' or '10090'
	auth = (type=="human") and 'NCBI' or 'GRCm'
	version = (type == "human") and '37' or '38'
	ucsc = (type=="human") and 'hg19' or 'mm10'
	bit = (type=="human") and 'hg19.2bit' or 'mm10.2bit'
	bb = (type=="human") and 'gencode.bb' or 'gencodeM2.bb'
	trix = (type=="human") and 'geneIndex.ix' or 'gencodeM2.ix'
		
	Chrom =  """
			chr: '21', 
			viewStart:  33031597, 
			viewEnd:  33041570, 
			cookieKey: '%s', 
			fullScreen: true,""" % type
	Coord =  """
			coordSystem: { 
			speciesName: '%s', 
			taxon: %s, 
			auth: '%s', 
			version: '%s', 
			ucscName: '%s'},""" % (type,taxon,auth,version,ucsc)
	source = """
			sources: 
				[{name: 'Genome',
				twoBitURI: 'URL/directory/%s',
				tier_type: 'sequence',
				provides_entrypoints: true,
				pinned: true}, 

				{name: 'GENCODE',
				bwgURI: 'URL/directory/%s',
				stylesheet_uri: 'URL/directory/gencode.xml',	
				collapseSuperGroups: true, 
				trixURI: 'URL/directory/%s',
				pinned:true}""" % (bit, bb, trix)
	newSource = string.replace(source,"URL",URL)
	newSource = string.replace(newSource,"directory",type)
	f.write(documentHead)
	f.write(Chrom)
	f.write(Coord)
	f.write(newSource)

	for each in allFiles:
		if "bw" in each:
			track = """
				,{name: '%s',
				collapseSuperGroups:true,
				bwgURI: '%s/%s'}""" % (each,URL,each)
			f.write(track)
		elif "vcf.gz" in each and ".tbi" not in each:
			track = """
				,{name: '%s',
				uri: '%s/%s',
				tier_type: 'tabix',
				payload: 'vcf'} """ % (each, URL, each)
			f.write(track)
		else:
			print("%s is not a Bigwig/VCF File"%each)
		


	documentEnd = """
		]
   });
  	</script>
   	<div id=\"svgHolder\"></div>
   </div>
   </body>
</html>"""

	f.write(documentEnd)
	f.close()
	
		