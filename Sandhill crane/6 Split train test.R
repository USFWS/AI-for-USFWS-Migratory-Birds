
library (splitTools)
library (ranger)

setwd(file.path('C:', 'Users', 'bpickens','Desktop', 'SACR_detection'))

# Load and explore
data1 <- read.table ("ducks_crane_mix.csv",sep = ",",header=TRUE, fill=TRUE)

#######################
## Partition types: 
# Basic- random
# Stratified- evenly split by a variable 
# Grouped- data blocks are kept together
# 2 SPLITS!
part_image <- partition(data1$unique_image_jpg,type = "grouped", p = c(train =0.70, test = 0.30))

# OR 3 SPLITS
# part_image <- partition(data1$unique_image,type = "grouped", p =c(train =0.6, valid = 0.2, test = 0.2))

train1 <- data1[part_image$train,]
test1 <- data1[part_image$test,]
# test1 <- data1[part_image$valid,]

# Examine distribution of species by partition
table (train1$label)
table (test1$label)

# Completely random!
names (data1)
part_image <- partition(data1$parent_image,type = "basic", p = c(train =0.70, test = 0.30))

train1 <- data1[part_image$train,]
test1 <- data1[part_image$test,]

# Examine distribution of species by partition
table (train1$species)
table (test1$species)

## Write each split to a new table
write.table(test1,"C:\\Users\\bpickens\\Desktop\\Lstudio_sacr\\test1_grouped.csv", col.names=TRUE, row.names=FALSE, sep=",")

write.table(train1,"C:\\Users\\bpickens\\Desktop\\Lstudio_sacr\\train1_grouped.csv", col.names=TRUE, row.names=FALSE, sep=",")


