
# MICA annotation, part 1, Convert images in a folder to tabular data 
# MICA = Move Image Crops for Annotation

# Inputs: code = species identifier
# observ = observer name
# Each folder needs to be labeled: [code]_[observ]
# Please set the 2 input/output working directories below for your study; name will be automatically populated
code = "ROYT"
observ = "bp"

name = paste0(code, "_", observ)

# Set directory that contains these image folders
setwd(file.path('C:', 'Users', 'bpickens','Desktop', 'Crops',
                'Annotations_to_process', name))

##list files in  a folder 
file_list <- list.files ()
file_list

### Change the species = [code]
df = data.frame(species_A = code, object_id_jpg = I(file_list))
df$observer_A <- observ

# Set export directory
setwd(file.path('C:', 'Users', 'bpickens','Desktop', 'Crops'
                ,'New_annotations'))

name2 <- paste0("table", "_", code, "_", observ, ".csv")

## Write the table to export directory 
write.table(df, name2 , col.names=TRUE, row.names=FALSE, sep=",")

View(df)
