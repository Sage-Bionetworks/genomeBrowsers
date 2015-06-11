total <- list.files(".. Your file directory containing bigwig/BAM files..")

config(total, "human")
config <- function(files, directory) {
  conf <- file("tracks.conf")
  ##Don't want the files with .bai in it
  files <- files[!files%in%".bai"]
  #sapply through files, -> if bigwig, then do formatting for bigwig files (ifelse) else do BAM
  lines <- sapply(files, function(i) { 
    track <- paste("[tracks.", which(i==files), "]",sep="")
    class <- paste("storeClass = JBrowse/Store/SeqFeature/", ifelse(grepl("bw",i),"BigWig","BAM"),sep="")
    plot <- paste("type = JBrowse/View/Track/",ifelse(grepl("bw",i),"Wiggle/XYPlot","Alignments2"),sep="")
    uniq <- ifelse(grepl("bw",i),"autoscale = clipped_global",
                   paste("baiUrlTemplate = ../../raw/",directory,"/",i,".bai",sep=""))
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