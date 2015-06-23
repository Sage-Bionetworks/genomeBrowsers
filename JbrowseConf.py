import os
import csv

def createJbrowse(allFiles, directory="raw",data="human",append=False,meta_type="tumor"):
	count = 0
	##If you want to add on extra data to existing, then append=TRUE
	if append:
		f = open('tracks.conf','a+')
		metaData = open('trackMetaData.csv', 'ab')
		fieldnames = ['label', 'category','meta_type','datatype','key']
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
		f = open('tracks.conf','w')
		metaData = open('trackMetaData.csv', 'wb')
   		fieldnames = ['label', 'category','meta_type','datatype','key']
		writer = csv.DictWriter(metaData, fieldnames=fieldnames)
		writer.writeheader()
##Big wig file congiuration
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
		else:
			print("%s is not a Bigwig/VCF File"%each)

				
	metaData.close()
	f.close()

