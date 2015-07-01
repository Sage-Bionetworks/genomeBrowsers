#JbrowseConf.py

##Required

  Project -              Project name

  Jbrowse directory-     Where Jbrowse-1.11.6 is installed (path)

  Genome -               Input (human/mouse) - hg19 and mm10 supported

  Folder Path -          Full path of folder with datafiles

##optional arguments:

  -h, --help:            show this help message and exit


  -ref REFERENCE, --reference REFERENCE: Folder of DNA reference files (fasta/(bed file of all genes))
  -N, --needRef:         Need reference genome?
  -A, --add:           Append onto existing conf?
  -D, --download:        Download genome fasta files
  -C, --create:          Create Folder structure for project

  For fresh jbrowse:

  python [projectname] [jbrowse folder path] [human/mouse] [path of folder with data] -D -C -N