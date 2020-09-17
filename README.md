# Genome Browsers

## Jbrowse
### JbrowseConf.py

##### Required

```
  Project -              Project name

  Jbrowse directory-     Where Jbrowse-1.11.6 is installed (path)

  Genome -               Input (human/mouse) - hg19 and mm10 supported

  Folder Path -          Full path of folder with datafiles

```

##### optional arguments:
```
  -h, --help:            show this help message and exit

  -N, --needRef:         Need reference genome?
  
  -A, --add:           Append onto existing conf?
  
  -D, --download:        Download genome fasta files
  
  -C, --create:          Create Folder structure for project
```
##### Example: 

For fresh jbrowse:
```
python JbrowseConf.py [Project] [Jbrowse directory] [Genome] [Folder Path] -D -C -N
```
## Biodalliance
### CreateBDal.py
```
  -h, --help            show this help message and exit

  -cu CONTROLURL, --controlURL CONTROLURL: Takes in list of control URL
  
  -cau CASEURL, --caseURL CASEURL: Takes in list of case URL
  
  -cf CONTROLFILE, --controlFile CONTROLFILE: Takes in list of control files
  
  -caf CASEFILE, --caseFile CASEFILE: Takes in list of case files
  
  -g GENOME, --genome GENOME: Input (human/mouse) hg19 or mm10 genomes
```
