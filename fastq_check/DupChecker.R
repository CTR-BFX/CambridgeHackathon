
library(ggplot2)

wd <- "~/Documents/CTR-Groups/Steve_Charnock-Jones/PlasmaSeq"

setwd(wd)



data <- read.table("fq.check.table.ed.txt")

head(data)

png("PlasmaSeq_Dups.png", width = 1000, height = 1000)
ggplot(data, aes(x = V1, y = V2 )) + geom_point(size = 0.5, alpha=.5) + ylim(0,35000000) + xlim(0,35000000) + xlab("Line Number in FQ File") + ylab("Line Number in FQ File") + ggtitle("Fastq entry duplicate analysis of SLX-9342.D701_D504.HJ572BBXX.s_1.r_1.fq.gz")
dev.off()
