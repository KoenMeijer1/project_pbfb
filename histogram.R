#! /usr/bin/Rscript
SRR4242432_qualityscore <- read.table("outputdirectory/sample_qualityscore.txt", quote="\"", comment.char="")
qualityscore <- SRR4242432_qualityscore
library(ggplot2)

#creates a 5 x 5 inch image exported
png("qualityscores.png",    # create PNG for the histogram        
    width = 5*300,        # 5 x 300 pixels
    height = 5*300,
    res = 300,            # 300 pixels per inch
    pointsize = 8)        # smaller font size
#histogram of qualityscores
ggplot(qualityscore,aes(qualityscore))+geom_bar(aes  (fill=..count..))
dev.off() # close the png device
