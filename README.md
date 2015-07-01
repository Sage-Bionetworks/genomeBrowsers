#JbrowseConf.py

##Required

  Project -              Project name

  Jbrowse directory-     Where Jbrowse-1.11.6 is installed (path)

  Genome -               Input (human/mouse) - hg19 and mm10 supported

  Folder Path -          Full path of folder with datafiles

##optional arguments:

  -h, --help:            show this help message and exit

  -N, --needRef:         Need reference genome?
  
  -A, --add:           Append onto existing conf?
  
  -D, --download:        Download genome fasta files
  
  -C, --create:          Create Folder structure for project

  For fresh jbrowse:

  python [Project] [Jbrowse directory] [Genome] [Folder Path] -D -C -N