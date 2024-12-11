
library (raster)
library (rgdal)
library (sf)

# Input: Set working dir for ortho/mosaics
setwd(file.path('D:', 'SACR_mosaics_Mar18_19_final2'))

# Inputs: pred1 = table from detection inference depicting predictions: xmin, ymin, w, h
# output_csv = name of output table of georeferenced predictions 
# output_gis = name of shapefile to output
# gsd_cm = spatial resolution of image
# crs1 = utm proj of mosaic-- 14N= 32614 or 15N = 32615
pred1 <- read.table ("C:/Users/bpickens/Desktop/SACR_detection/demo1.csv", sep = ",", header=TRUE, fill=TRUE)
output_predictions = "D:/test_Dec11.csv"
export_spatial = "D:/test_Dec11.shp"
gsd_m = 0.103 
crs1 = 32614

## List files in dir and get extents
gridz <- list.files (pattern="*tif$")  
gridz

extents1 <- data.frame(raster_name=NA, xmin_extent=NA, xmax_extent=NA, ymin_extent=NA, ymax_extent=NA)

for (f in gridz){
  r1 <- raster(f)
  e1 <- extent(r1)
  raster_name <- f
  xmin_extent <- e1[1,]
  xmax_extent <- e1[2,]
  ymin_extent <- e1[3,]
  ymax_extent <- e1[4,]
  vector1 <- c(raster_name, xmin_extent, xmax_extent, ymin_extent, ymax_extent)
  print(vector1)
  extents1 <- rbind(extents1, vector1)
}

extents1$unique_image_jpg <- extents1$raster_name
extents1$raster_name <- NULL

## Merge with predictions
pred1$basename <- basename(pred1$unique_image_jpg)
pred1$unique_image_jpg <- pred1$basename
pred1$basename <- NULL

merge1 <- merge(extents1, pred1, by="unique_image_jpg") 

# m = abbreviated for meters
merge1$xmin_m <- merge1$xmin*gsd_m
merge1$ymin_m <- merge1$ymin*gsd_m
merge1$h_m <- (merge1$h*gsd_m)/2
merge1$w_m <- (merge1$w*gsd_m)/2

# x_annot, y_annot = coordinates for annotations
class(merge1$xmin_extent)

merge1$xmin_extent <- as.numeric(merge1$xmin_extent)
merge1$ymax_extent <- as.numeric(merge1$ymax_extent)

merge1$x_annot <- merge1$xmin_extent + ((merge1$xmin_m)+ merge1$w_m)

merge1$y_annot <- merge1$ymax_extent - ((merge1$ymin_m)+ merge1$h_m)
merge1$y_annot_above <- merge1$y_annot + 0.40

merge1$x_annot <- as.numeric(merge1$x_annot)
merge1$y_annot <- as.numeric(merge1$y_annot)
merge1$y_annot_above <- as.numeric(merge1$y_annot_above)
merge1$xmax_extent <- NULL
merge1$ymax_extent <- NULL

merge1[0:5,]

write.table(merge1, output_predictions, sep=",", row.names=FALSE)

## Make shapefile
# get rid of na's first
merge2 <- merge1[complete.cases(merge1), ]

# Projections, crs = 4326--WGS84
new_sf <- st_as_sf(merge2, coords = c("x_annot", "y_annot_above"), crs= crs1)

st_write(new_sf, export_spatial, driver = "ESRI Shapefile")  






