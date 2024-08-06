
library (raster)
library (rgdal)

setwd(file.path('C:', 'Users', 'bpickens','Desktop', 'SACR_detection', 'results_survey',
                'dropout_results'))

## Inputs
data1 <- read.table ("predict_mosaic_duck_goose_dropout4.csv",sep = ",", 
                     header=TRUE, fill=TRUE)
gsd_m = 0.103 
output_predictions <- "predict_duck_goose_dropout5.csv"


data1$xmin_m <- data1$xmin*gsd_m
data1$ymin_m <- data1$ymin*gsd_m

data1$h_m <- (data1$h*gsd_m)/2
data1$w_m <- (data1$w*gsd_m)/2

# data1[0:5,]

data1$xmin_extent <- data1$xmin_exten
data1$ymin_extent <- data1$ymin_exten
data1$xmax_extent <- data1$xmax_exten
data1$ymax_extent <- data1$ymax_exten


data1$ymax_exten <- NULL
data1$xmax_exten <- NULL
data1$y_annot_ab <- NULL


data1$x_annot <- data1$xmin_extent + ((data1$xmin_m)+ data1$w_m)
data1$y_annot <- data1$ymax_extent - ((data1$ymin_m)+ data1$h_m)
data1$y_annot_above <- data1$y_annot + 0.40

data1$x_annot <- as.numeric(data1$x_annot)
data1$y_annot <- as.numeric(data1$y_annot)
data1$y_annot_above <- as.numeric(data1$y_annot_above)

write.table(data1, output_predictions, sep=",", row.names=FALSE)
