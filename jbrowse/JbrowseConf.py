import csv
import string
import os
import argparse
import synapseclient
import webbrowser

syn = synapseclient.Synapse()
syn=syn.login()
#x="ls"
#y=`eval $x`
#echo $y <- all the files in the folder
#sed 'Nd' file > newfile <- where N is the line in the file
#sort -k1,1 -k2,2n H9.102.2.5__exon.bed > sorted.bed <- sorting bed files (All bed/VCF files have to be sorted before indexing) 
#chromosome and start position matter
parser = argparse.ArgumentParser()
#positional arguments
parser.add_argument("Project", metavar='Project',type=str, help='Project name')
parser.add_argument("Jbrowse", metavar='Jbrowse directory', type=str, help= "Where Jbrowse-1.11.6 is installed (path)")
parser.add_argument("Genome",metavar='Genome',type=str,help="Input (human/mouse) - hg19 and mm10 supported")
parser.add_argument("FolderPath",metavar='Folder Path',type=str,help="Full path of folder with datafiles")


#Optional arguments
parser.add_argument("-ref","--reference", action="store",default="Reference",help= "Folder of DNA reference files (fasta/(bed file of all genes))")
parser.add_argument("-N","--needRef",action='store_true',help="Need reference genome?")
parser.add_argument("-A","--add",action='store_true',help="Append onto existing conf?")
parser.add_argument("-D","--download",action='store_true',help="Download genome fasta files")
parser.add_argument("-C","--create", action="store_true",help="Create Folder structure for project")


args = parser.parse_args()
#Required
genome = args.Genome
jbrowse = args.Jbrowse
project = args.Project
folderpath = args.FolderPath
#Optional
files =  args.files
urls = args.url
ref = args.reference
needRef = args.needRef
add = args.add
download = args.download
create = args.create

if create:
	os.mkdir(os.path.join(jbrowse,project))
	os.mkdir(os.path.join(jbrowse,project,"json"))
	os.mkdir(os.path.join(jbrowse,project,"raw"))
	os.mkdir(os.path.join(jbrowse,project,"json",genome))
	os.mkdir(os.path.join(jbrowse,project,"raw",genome))

#This is where the configuration file goes
output = os.path.join(project,"json",genome)##for right now <- genome is the subfolder name
rawfiles = os.path.join(project,"raw",genome)

os.system("ln -s %s %s" %(folderpath,os.path.join(project,"raw")))
os.system("mv %s %s"%(os.path.join(project,"raw","*"),rawfiles))

def createRefGenome(directory):
	##If the person doesn't have the fasta files, then download them from synapse
	if download:
		os.mkdir(os.path.join(jbrowse,"Reference"))
		os.mkdir(os.path.join(jbrowse,"Reference",genome))
		if genome=="human":
			temp = syn.query('SELECT id, name FROM entity WHERE parentId == "syn4557835"')
		else:
			temp = syn.query('SELECT id, name FROM entity WHERE parentId == "syn4557836"')
		for each in temp['entity.id']:
			syn.get(temp,downloadLocation = "%s" %(directory))
		
	#Gives list of filenames but with the path appended to it
	filelist = [os.path.join(directory,filenames) for filenames in os.listdir(directory)]
	for each in filelist:
		if ".fa" in each: # This gives the DNA seqs
			os.system("perl %s/bin/prepare-refseqs.pl --fasta %s --out %s" % (jbrowse,each,os.path.join(jbrowse,output))) 
		elif ".bed" in each: #This gives the genes (this bed file is already formatted)
			os.system("""perl %s/bin/flatfile-to-json.pl --bed %s --trackType CanvasFeatures --trackLabel human_genes --config '{"maxFeatureScreenDensity":20,"maxHeight":300}' --clientConfig '{"strandArrow": false,"color":"cornflowerblue"}' --out %s""" %(jbrowse,each,os.path.join(jbrowse,output)))
	os.system("perl %s/bin/generate-names.pl -v --out %s"%(jbrowse,os.path.join(jbrowse,output))) 

##If the reference files aren't already local, then have to get the reference files
if needRef:
 	createRefGenome(os.path.join(jbrowse,ref,genome))
##since the folders should be formatted prior to running this script. All files should be under 
##(Project folder)/(raw)/(human)
def createJbrowse(allFiles, directory="raw",data="human",append=False,meta_type="tumor"):
	count = 0
	##If you want to add on extra data to existing, then append=TRUE
	if append:
		f = open(os.path.join(jbrowse,output,'tracks.conf'),'a+')
		metaData = open(os.path.join(jbrowse,output,'trackMetadata.csv'), 'ab')
		fieldnames = ['label', 'category','meta_type','datatype','key'] ##Hardcoded fields
		writer = csv.DictWriter(metaData, fieldnames=fieldnames)
##This gets the track info [...] So that you can get the track number
		f.seek(0)
		lines = f.readlines()
		for each in lines:
		    if "tracks" in each:
		        words = each.split()
		        for word in words:
		            num = word.split(".")
		            if len(num)==2:
	                	count = int(num[1])+1
	else: ##Open fresh tracks and trackmetadata
		f = open(os.path.join(jbrowse,output,'tracks.conf'),'w')
		metaData = open(os.path.join(jbrowse,project,'trackMetaData.csv'), 'wb')
   		fieldnames = ['label', 'category','meta_type','datatype','key'] ##Hardcoded fields
		writer = csv.DictWriter(metaData, fieldnames=fieldnames)
		writer.writeheader()
###########Big wig file congiuration#######
	for each in allFiles:
		if "bw" in each:
			category = "Human_Coverage"
			datatype = "bigwig"
			track = """
[ tracks.%s ]
storeClass  = JBrowse/Store/SeqFeature/BigWig
urlTemplate = ../../%s/%s/%s

metadata.category = %s
metadata.type = %s
metadata.datatype = %s
type     = JBrowse/View/Track/Wiggle/XYPlot
key      = %s
autoscale = clipped_global\n""" % (count,directory,data,each,category,meta_type,datatype,each)
			f.write(track)
			writer.writerow({'label':count, 'category':category,'meta_type':meta_type,'datatype':datatype,'key':each})
			count+=1
		#####VCF FILES#######
		#VCF file configuration Make sure the .tbi file exists. Jbrowse config auto searches for this file.
		elif "vcf.gz" in each and ".tbi" not in each:
			category = "Variant"
			datatype = "VCF"
			track = """

[ tracks.%s ]
storeClass     = JBrowse/Store/SeqFeature/VCFTabix
urlTemplate    = ../../%s/%s/%s

metadata.category = %s
metadata.type = %s
metadata.datatype = %s
# settings for how the track looks
type = JBrowse/View/Track/CanvasVariants
key  = %s\n"""% (count,directory,data,each,category,meta_type,datatype,each)

			f.write(track)
			##Write each line of the metadata.csv
			writer.writerow({'label':count, 'category':category,'meta_type':meta_type,'datatype':datatype,'key':each})
			count+=1
		####BAM FILES####
		#baiUrlTemplate can we used to get exact location of bai file
		elif ".bam" in each and ".bai" not in each:
			category = "Alignment"
			datatype = "BED"
			track = """			
[tracks.%s]
storeClass = JBrowse/Store/SeqFeature/BAM
urlTemplate = ../../%s/%s/%s

metadata.category = %s
metadata.type = %s
metadata.datatype = %s
type = JBrowse/View/Track/Alignments2
key = %s\n"""%(count,directory,data,each,category,meta_type,datatype,each)

			f.write(track)
			##Write each line of the metadata.csv
			writer.writerow({'label':count, 'category':category,'meta_type':meta_type,'datatype':datatype,'key':each})
			count+=1
		#elif ".bed" in each and ".gz" not in each:
		#	os.system("perl %s/bin/flatfile-to-json.pl --bed %s --trackLabel %s --trackType CanvasFeatures" % (jbrowse,each,each))
		else:
			print("%s is not a Bigwig/VCF/BAM File"%each)
	metaData.close()
	f.close()
	#url = "http://localhost/JBrowse-1.11.6/?data=%s/json/%s" %(project,genome)
	#webbrowser.open(url,new=2)

dataFiles = os.listdir(os.path.join(jbrowse,rawfiles))
createJbrowse(dataFiles,data=genome,append =add)