### CONVERT YOLO LABEL FILES (.TXT) TO A CSV
library (tidyr)
library (dplyr)
library (filenamer)
library(readr)
library (stringr)
library (plyr)

# IMPORTANT: Remove any empty txt files among your label files (check if size, kb =0); 
# those are not needed for yolo implementation

# Enter your directory
setwd(file.path('C:', 'temp', 'sacr_modelx', 'May23_dataset', 'train', 'labels'))

# Enter the name of csv to export
export_csv = "export_train.csv"

# Parent image dimensions
parent_width = 736
parent_height = 736

# Optional: class index to class name
## Add more classes as needed

label_name0 = "duck_goose"
label_name1 = "sandhill_crane"

## List files in folder 
file_list <- list.files() # uses setwd 
file_list

## change text to csv
filelist = list.files(pattern = ".txt")

files <- list.files(pattern = ".txt")
find_error <- lapply(seq_along(files), function(x) {
tryCatch(  {
  dt <- read.table(files[x], header = F, sep = ' ')
    dt$index <- x   # or files[x] is you want to use the file name instead
    dt
    },
    error=function(e) { NULL }
  )
 })

myData_list <- lapply(files, function(x) {
  out <- data.table::fread(x, header = FALSE)
  out$source_file <- x
  return(out)
})

data2 <- data.table::rbindlist(myData_list)

new_headers <- c("class_index", "center_w", "center_h", "w", "h" , "unique_image_jpg")
colnames(data2) <- new_headers  

## Optional- change class index to class name
data2$class <- gsub ("0", label_name0, data2$class)
data2$class <- gsub ("1", label_name1, data2$class)
## Add more classes as needed

data2[0:6,]

data2$unique_image_jpg <- gsub (".txt", ".jpg", data2$unique_image_jpg)

data2$w <- data2$w *parent_width
data2$h <- data2$h *parent_height
data2$xmin <- (data2$center_w*parent_width)-(data2$w/2) 
data2$ymin <- (data2$center_h*parent_height)-(data2$h/2)
data2$center_h <- NULL
data2$center_w <- NULL

data2$h <- ceiling(data2$h)
data2$w <- ceiling(data2$w)
data2$xmin <- ceiling(data2$xmin)
data2$ymin <- ceiling(data2$ymin)

data2$basename <- substr(data2$unique_image, 1, nchar(data2$unique_image)-4)

data2$unique_BB <- paste0(data2$basename, "_", data2$xmin,"_", data2$ymin, "_", data2$w, "_", data2$h,".jpg")
data2$unique_BB

View(data2)
table(data2$class)

write.table(data2, export_csv, sep=",", row.names=FALSE)
