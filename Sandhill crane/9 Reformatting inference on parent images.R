
library (tidyr)
library(stringr)
library(tidyverse)

# Set working directory
setwd(file.path('C:', 'Users', 'bpickens','Desktop', 'SACR_detection', 'RESULTS',
                'survey_results'))

# Inputs: data1 = csv from YOLO inference results
# new_csv = new csv result file to export
data1 <- read.table ("sacr_yolov5x_survey_conf05.csv",sep = ",", 
                     header=TRUE, fill=TRUE)

new_csv <- "sacr_yolov5x_survey_conf05_step2.csv"

# Reformat score, class
data1$score <- gsub("PredictionScore: <value: ", "", data1$score)
data1$score <- gsub(">", "", data1$score)

data1$class <- gsub("Category: <id: 1, name: sandhill_crane>", "sandhill_crane", data1$class)
data1$class <- gsub("Category: <id: 0, name: duck_goose>", "duck_goose", data1$class)
  
data1$bbox <- gsub("BoundingBox: <" , "", data1$bbox)
data1$bbox <- gsub("w: " , "", data1$bbox)

data1$bbox <- gsub("h: " , "", data1$bbox)
data1$bbox <- gsub(">" , "", data1$bbox)
data1$bbox <- gsub("\\(" , "", data1$bbox)


data3 <-separate_wider_delim (data1, cols= "bbox", delim=",", names= c("xmin", "ymin", "xmax", "ymax", "w","h"))
data2 <- data3

data2$xmax <- NULL
data2$ymax <- NULL

data2$xmin <- as.numeric(data2$xmin)
data2$ymin <- as.numeric(data2$ymin)
data2$w <- as.numeric(data2$w)
data2$h <- as.numeric(data2$h)

data2$basename <- basename(data2$unique_image_jpg)

data2$basename2 = substr(data2$basename,1,nchar(data2$basename)-4)

data2$unique_BB <- paste(data2$basename2, data2$xmin, data2$ymin, 
                         data2$w, data2$h, sep = "_")

data2$unique_image_jpg <- NULL
data2$basename2 <- NULL
data2$unique_image_jpg <- data2$basename
data2$unique_image_jpg <- data2$basename
data2$basename <- NULL
data2$score <- signif(data2$score, digits=2)

data2$unique_tile_jpg <- data2$unique_image_jpg
data2$unique_image_jpg <- NULL

data2$unique_image_jpg <- substr(data2$unique_tile_jpg,1,nchar(data2$unique_tile_jpg)-11)

# Count cranes
data2$sandhill_crane <- data2$class
data2$sandhill_crane <- gsub("sandhill_crane", 1,  data2$sandhill_crane)
data2$sandhill_crane <- gsub("duck_goose", 0, data2$sandhill_crane)
data2$sandhill_crane <- as.integer(data2$sandhill_crane)

#count ducks/geese
data2$duck_goose <- data2$class
data2$duck_goose <- gsub("sandhill_crane", 0,  data2$duck_goose)
data2$duck_goose <- gsub("duck_goose", 1, data2$duck_goose)
data2$duck_goose <- as.integer(data2$duck_goose)

data3 <- data2[, c("class", "score", "xmin", "ymin", "w", "h", "duck_goose", "sandhill_crane", "unique_image_jpg")]
  
### write table
write.table(data3,new_csv, sep=",", row.names=FALSE)
