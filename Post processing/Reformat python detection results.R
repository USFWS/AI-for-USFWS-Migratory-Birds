
library (tidyr)
library(stringr)
library(tidyverse)
                         
setwd(file.path('C:', 'Users', 'Aware', 'Desktop'))

# Inputs: data1 = data tables resulting from YOLO run with columns of
# score, class, bbox
#   new_csv = name of new results file
data1 <- read.table ("D:/AMAPPS/YOLOv8_2024_Aug26.csv",sep = ",", 
                     header=TRUE, fill=TRUE)

# Input name newly formatted csv and RuN!
new_csv <- "D:/AMAPPS/YOLOv8_2024_Aug26_reformat.csv"

# fix score, class
data1$score <- gsub("PredictionScore: <value: ", "", data1$score)
data1$score <- gsub(">", "", data1$score)

data1$class <- gsub("Category: <id: 0, name: bird>", "bird", data1$class)
data1$class <- gsub("Category: <id: 2, name: nonbird>", "mammal", data1$class)

data1$class <- gsub("Category: <id: 1, name: manmade>", "manmade", data1$class)
  
data1$bbox <- gsub("BoundingBox: <" , "", data1$bbox)
data1$bbox <- gsub("w: " , "", data1$bbox)

data1$bbox <- gsub("h: " , "", data1$bbox)
data1$bbox <- gsub(">" , "", data1$bbox)
data1$bbox <- gsub("\\(" , "", data1$bbox)
data1$bbox

data2 <-separate_wider_delim (data1, cols= "bbox", delim=",", names= c("xmin", "ymin", "xmax", "ymax", "w","h"))

data2$xmax <- NULL
data2$ymax <- NULL

data2$xmin <- as.integer(data2$xmin)
data2$ymin <- as.integer(data2$ymin)
data2$w <- as.integer(data2$w)
data2$h <- as.integer(data2$h)
data2$unique_image_jpg
data2$basename <- basename(data2$unique_image_jpg)
data2$basename2 = substr(data2$basename,1,nchar(data2$basename)-4)
data2$unique_BB <- paste(data2$basename2, data2$xmin, data2$ymin, 
                         data2$w, data2$h, sep = "_")

data2$unique_image_jpg <- NULL
data2$basename2 <- NULL
data2$unique_image_jpg <- data2$basename
data2$unique_image_jpg <- data2$basename
data2$basename <- NULL
data2$score <- as.numeric(data2$score)
data2$score <- signif(data2$score, digits=2)

data3 <- data2[, c("class", "score", "xmin", "ymin", "w", "h", "unique_image_jpg",
                   "unique_BB")]

### write table
write.table(data3,new_csv, sep=",", row.names=FALSE)

