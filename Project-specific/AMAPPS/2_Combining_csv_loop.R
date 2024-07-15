
# Make a backup copy of your .aflight file first!!!!
library (tidyr)
library (dplyr)
library (filenamer)
library(readr)

# Enter your directory
# setwd(file.path('D:', 'WOST_metadata', '2023_image_metadata_indiv'))


# Enter your directory
setwd(file.path('C:', 'Users', 'bpickens','Desktop', 'Seabird_aflights', 'Images_for_loop'))

## List files in folder 
file_list <- list.files() # uses setwd 
file_list

# Loops through all .csv and binds them
df1 <- file_list %>%
  lapply(read.csv) %>%
  bind_rows

## temp. correction for time variable
#library(chron)
#df1$time <- chron (times=df1$time)

write.table(df1, "2024_images_metadata_update_April15.csv", sep=",", row.names=FALSE)


