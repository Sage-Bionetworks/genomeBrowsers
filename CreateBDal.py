import string
import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-cu","--controlURL",action="store",help="Takes in list of control URL")
parser.add_argument("-cau","--caseURL",action="store",help="Takes in list of case URL")
parser.add_argument("-cf","--controlFile",action="store",help="Takes in list of control files")
parser.add_argument("-caf","--caseFile",action="store",help="Takes in list of case files")
parser.add_argument("-g","--genome",action = "store",default = "human",help= "Input (human/mouse) hg19 or mm10 genomes")
parser.add_argument("-url","--url",action="store",default = "http://localhost",help = "URL of files")
args = parser.parse_args()

cURL =  args.controlURL
caURL =  args.caseURL
caFile = args.caseFile
cFile =  args.controlFile
urls = args.url
#
#if cURL:
#	cURL = cURL.split()
#else:
#	cURL = []
#
#if caURL:
#	caURL = caURL.split()
#else:
#	caURL = []

#if caFile:
#	caFile = caFile.split()
#	for each in caFile:
#		temp  = "/".join([urls,each])
#		caURL.append(temp)
#else:
#	caFile= []

#if cFile:
#	cFile = cFile.split()
#	for each in cFile:
#		temp = "/".join([urls,each])
#		cURL.append(temp)
#else:
#	cFile=[]



def create_track(allFiles,URL,f,case):
	if case: #If case files, data should be in case folder
		subfolder = "case"
		style = """
					,style: [{type : 'default',
							style: {glyph: 'HISTOGRAM',
									COLOR1:'red',
									COLOR2:'red',
									COLOR3:'red',
									HEIGHT:30}}]}"""
	else:
		subfolder = "control"
		style = ""

	if allFiles:
		allFiles = allFiles.split()
		for each in allFiles:
			if "bw" in each:
				##If it is a case file, then the histograms should be red
				track = """
					,{name: '%s',
					collapseSuperGroups:true,
					bwgURI: '%s/%s/%s'%s}""" % (each,URL,subfolder,each,style)
				f.write(track)
			elif "vcf.gz" in each and ".tbi" not in each:
				track = """
					,{name: '%s',
					uri: '%s/%s/%s',
					tier_type: 'tabix',
					payload: 'vcf'} """ % (each, URL, subfolder,each)
				f.write(track)
			else:
				print("%s is not a Bigwig/VCF File"%each)





#files=next(os.walk("/Library/WebServer/Documents/"))[2]
def createBioHTML(caseURL,controlURL,caseFile,controlFile, URL="http://localhost", folder="human"):
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
		
	<script language="javascript" src="%s/dalliance-compiled.js"></script> 
	<script language="javascript">
		new Browser({ """% URL

	taxon = (folder=="human") and '9606' or '10090'
	auth = (folder=="human") and 'NCBI' or 'GRCm'
	version = (folder == "human") and '37' or '38'
	ucsc = (folder=="human") and 'hg19' or 'mm10'
	bit = (folder=="human") and 'hg19.2bit' or 'mm10.2bit'
	bb = (folder=="human") and 'gencode.bb' or 'gencodeM2.bb'
	trix = (folder=="human") and 'geneIndex.ix' or 'gencodeM2.ix'
		
	Chrom =  """
			chr: '21', 
			viewStart:  33031597, 
			viewEnd:  33041570, 
			cookieKey: '%s', 
			fullScreen: true,""" % folder
	Coord =  """
			coordSystem: { 
			speciesName: '%s', 
			taxon: %s, 
			auth: '%s', 
			version: '%s', 
			ucscName: '%s'},""" % (folder,taxon,auth,version,ucsc)
	colors = """
			baseColors: {
                 'A': 'black',
                 'C': 'black',
                 'G': 'black',
                 'T': 'black',
                 '-': 'black', //deletion
                 'I': 'red'    //insertion
            },"""
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
	newSource = string.replace(newSource,"directory",folder)
	f.write(documentHead)
	f.write(Chrom)
	f.write(Coord)
	f.write(colors)
	f.write(newSource)

	create_track(caseURL,URL,f,True)
	create_track(controlURL,URL,f,False)
	create_track(caseFile,URL,f,True)
	create_track(controlFile,URL,f,False)

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
	


createBioHTML(caURL,cURL,caFile,cFile,URL = urls,folder = args.genome)	
