library(tools)
total <- list.files(".. Your file directory containing bigwig/BAM files..")
##config((list of files here),(type of file-belongs to humans/mouse/etc...))
config(total, "human")
total<- list.files()

config <- function(files, directory) {
  conf <- file("tracks.conf")
  ##Don't want the files with .bai in it
  tfiles <- files[file_ext(files) %in% c("bw","bam")]
  #sapply through files, -> if bigwig, then do formatting for bigwig files (ifelse) else do BAM
  #'
  #'@track Unique trackname
  #'@class choose bigwig/BAM configuration
  #'@plot bigwig - plots XY/ Density, BAM - plots alignment2
  #'@uniq bigwig - autoscaling, BAM - Attach BAI file
  #'@cat Put into category
  #'@key Name of track
  #'
  if (length(tfiles) ==0) {
    stop("Files passed in are neither BAM or bigwig format")
  } 
  lines <- sapply(tfiles, function(i) { 
    track <- paste("[tracks.", which(i==files), "]",sep="")
    class <- paste("storeClass = JBrowse/Store/SeqFeature/", ifelse(grepl("bw",i),"BigWig","BAM"),sep="")
    plot <- paste("type = JBrowse/View/Track/",ifelse(grepl("bw",i),"Wiggle/XYPlot","Alignments2"),sep="")
    uniq <- ifelse(grepl("bw",i),"autoscale = clipped_global",
                   paste("baiUrlTemplate = ../../raw/",directory,"/",i,".bai",sep="")) ##add .bai if bam file
    cat <- paste("metadata.category = ",directory,ifelse(grepl("bw",i),"/ Coverage","/ Reads"),sep="")
    temp <- paste("urlTemplate = ../../raw/",directory,"/",i,sep="")
    key <- paste("key = ",i,sep="")
    return (c(track,class,temp,cat,plot,key,uniq))
    
    ##Chunky if else statement, but may need if other file types come into existence
   # if (grepl("bw",i)) {
    #  class <- "storeClass = JBrowse/Store/SeqFeature/BigWig"
    #  plot <- "type = JBrowse/View/Track/Wiggle/XYPlot"
    #  uniq <- "autoscale = clipped_global"
    #  cat <- paste("metadata.category = ",directory,"/ Coverage",sep="")
    #} else {
    #  class <- "storeClass = JBrowse/Store/SeqFeature/BAM"
    #  plot <- "type = JBrowse/View/Track/Alignments2"
    #  uniq <- paste("baiUrlTemplate = ../../raw/",directory,"/",i,".bai",sep="")
    #  cat <- paste("metadata.category = ",directory,"/ Reads",sep="")
    #}
  }) 
  writeLines(lines, conf)
  close(conf)
}