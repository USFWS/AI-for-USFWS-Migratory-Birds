### CONVERT YOLO LABEL FILES (.TXT) TO A CSV

library (tidyr)
library (dplyr)
library (filenamer)
library(readr)
library (stringr)

# IMPORTANT: Remove any empty txt files among your label files (check if size, kb =0); 
# those are not needed for yolo implementation

# Enter your directory
setwd(file.path('C:', 'Users', 'bpickens','Desktop', 'SACR_detection', 'sacr_dataset_batch1_Feb20', 'train', 'labels'))

# Enter the name of csv to export
export_csv = "C:/users/bpickens/Desktop/SACR_detection/RESULTS/gt_train_batch1_Feb20.csv"

# Optional: class index to class name
## Add more classes as needed

#label_name0 = "duck_goose"
#label_name1 = "sandhill_crane"

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

my_data <- data.table::rbindlist(myData_list)

new_headers <- c("class_index", "center_w", "center_h", "w", "h" , "unique_image")
colnames(my_data) <- new_headers  

## Optional- change class index to class name
my_data$class <- gsub ("0", label_name0, my_data$class)
my_data$class <- gsub ("1", label_name1, my_data$class)
## Add more classes as needed

write.table(my_data, export_csv, sep=",", row.names=FALSE)
